from typing import List
from urllib.parse import urlparse

import pymupdf
import scrapy
from app.utils import BLOCKED_DOMAINS, SCORING_PAGE_COUNT, setup_logger
from app.vectorisation import Vectorisation
from dotenv import load_dotenv
from langchain_core.documents import Document
from pymupdf import Page
from scrapy.exceptions import CloseSpider

load_dotenv()

logger = setup_logger(__name__)


class ReversePDFScraperSpider(scrapy.Spider):
    name = "reverse-pdf-scraper"

    def __init__(self, context: str, reference_document: str, *args, **kwargs):
        super(ReversePDFScraperSpider, self).__init__(*args, **kwargs)
        self.context = context
        self.reference_document = reference_document
        logger.info(f"Context: {self.context}")
        logger.info(f"Reference document: {self.reference_document}")

    async def start(self):
        try:
            with pymupdf.open(self.reference_document) as doc:
                vectorisation = Vectorisation()
                urls = self.get_urls(doc)
                similarity_score = vectorisation.context_similarity_score(
                    self.context, doc[:SCORING_PAGE_COUNT]
                )

            self.initial_threshold = similarity_score / 2
            logger.info(
                f"Similarity score: {similarity_score} | Initial threshold: {self.initial_threshold}"
            )

            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            logger.error(str(e))
            CloseSpider(str(e))

    def should_skip(self, uri):
        parser = urlparse(uri)
        if parser.scheme not in ["http", "https"]:
            return True
        hostname = parser.hostname or ""
        return any(blocked in hostname for blocked in BLOCKED_DOMAINS)

    def get_urls(self, doc: List[Page]) -> List[str]:
        urls = []
        for page in doc:
            for link in page.get_links():
                uri = link.get("uri")
                if (uri) and (uri not in urls) and (not self.should_skip(uri)):
                    urls.append(uri)
        return urls

    def get_urls_and_docs(self, response) -> tuple[List[str], List[Document]]:
        with pymupdf.Document(stream=response.body) as doc:
            return self.get_urls(doc), [
                Document(
                    page_content=page.get_text(),
                    metadata={
                        "source": response.url,
                        "page": page.number + 1,
                        "total_size": len(response.body),
                    },
                )
                for page in doc
            ]
        return [], []

    def parse(self, response):
        content_type = response.headers.get("Content-Type", "").decode("utf-8").lower()
        if "pdf" in content_type:
            urls, docs = self.get_urls_and_docs(response)
            yield {
                "url": response.url,
                "docs": docs,
                "total_size": len(response.body),
                "initial_threshold": self.initial_threshold,
            }
            for url in urls:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )
        elif "html" in content_type:
            for uri in response.css("a::attr(href)").getall():
                if self.should_skip(uri):
                    continue
                yield response.follow(
                    uri,
                    callback=self.parse,
                )
