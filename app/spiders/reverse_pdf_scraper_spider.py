import os
import time
import uuid
from typing import List
from urllib.parse import urlparse

import pymupdf
import scrapy
from app.milvus import Milvus
from app.utils import (
    BLOCKED_DOMAINS,
    NUMBER_OF_PAGES_TO_CHECK,
    SIMILARITY_THRESHOLD,
    setup_logger,
)
from dotenv import load_dotenv
from langchain_community.utils.math import cosine_similarity
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from pymupdf import Page

load_dotenv()

logger = setup_logger(__name__)


class ReversePDFScraperSpider(scrapy.Spider):
    name = "reverse-pdf-scraper"

    def __init__(self, topics: str, document_path: str, *args, **kwargs):
        super(ReversePDFScraperSpider, self).__init__(*args, **kwargs)
        self.model_embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("DENSE_MODEL"),
        )
        self.splitter = SentenceTransformersTokenTextSplitter(
            model_name=os.getenv("DENSE_MODEL"),
        )
        self.milvus = Milvus()
        self.topics = topics.split(",")
        self.document_path = document_path

        logger.info(f"Topics: {self.topics}")
        logger.info(f"Document: {self.document_path}")

    def should_skip(self, url):
        parser = urlparse(url)
        if parser.scheme not in ["http", "https"]:
            return True
        hostname = parser.hostname or ""
        return any(blocked in hostname for blocked in BLOCKED_DOMAINS)

    async def start(self):
        with pymupdf.open(self.document_path) as doc:
            uris = self.get_links(doc)
            for uri in uris:
                yield scrapy.Request(url=uri, callback=self.parse)

    def get_links(self, doc: List[Page]) -> List[str]:
        uris = []
        for page in doc:
            for link in page.get_links():
                uri = link.get("uri")
                if (uri) and (uri not in uris) and (not self.should_skip(uri)):
                    uris.append(uri)
        return uris

    def is_topics_similar(self, topics: List[str], doc: List[Page]) -> bool:
        if not topics:  # Pass checking if no topics provided
            return True

        pages = [" ".join([page.get_text() for page in doc])]
        pages_embedding = self.model_embeddings.embed_documents(pages)
        topic_embeddings = self.model_embeddings.embed_documents(topics)
        similarities = cosine_similarity(topic_embeddings, pages_embedding)

        for topic, similarity in zip(topics, similarities):
            logger.info(f"Similarity score: {similarity[0]}")
            if similarity[0] >= SIMILARITY_THRESHOLD:
                return True
        return False

    def process_pdf(self, response) -> List[str]:
        duplicate = self.milvus.is_duplicate(
            source=response.url,
            total_size=len(response.body),
        )
        uris = []
        with pymupdf.Document(stream=response.body) as doc:
            uris = self.get_links(doc)
            if not duplicate:
                similar = self.is_topics_similar(
                    self.topics, doc[:NUMBER_OF_PAGES_TO_CHECK]
                )
                if not similar:
                    return []

                def document_generator():
                    for page in doc:
                        yield Document(
                            page_content=page.get_text(),
                            metadata={
                                "source": response.url,
                                "page": page.number + 1,
                                "total_size": len(response.body),
                            },
                        )

                chunks = self.splitter.split_documents(document_generator())
                dense_vectors = self.model_embeddings.embed_documents(
                    [chunk.page_content for chunk in chunks]
                )
                inserted = self.milvus.insert_data(
                    [
                        {
                            "id": str(uuid.uuid4()),
                            "dense_vector": dense_vector,
                            "text": chunk.page_content,
                            "source": chunk.metadata["source"],
                            "page": chunk.metadata["page"],
                            "total_size": chunk.metadata["total_size"],
                            "timestamp": int(time.time() * 1000),
                        }
                        for chunk, dense_vector in zip(chunks, dense_vectors)
                    ]
                )
                if inserted.get("insert_count", 0) > 0:
                    logger.info(
                        f"Successfully inserted {inserted['insert_count']} data of {response.url}"
                    )
        return uris

    def parse(self, response):
        content_type = response.headers.get("Content-Type", "").decode("utf-8").lower()
        if "pdf" in content_type:
            uris = self.process_pdf(response)
            for uri in uris:
                yield scrapy.Request(
                    url=uri,
                    callback=self.parse,
                )
        elif "html" in content_type:
            for link in response.css("a::attr(href)").getall():
                if self.should_skip(link):
                    continue
                yield response.follow(
                    link,
                    callback=self.parse,
                )
