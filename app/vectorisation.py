import os
import time
import uuid
from typing import List

from app.utils import setup_logger
from dotenv import load_dotenv
from langchain_community.utils.math import cosine_similarity
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from pymupdf import Page

load_dotenv()

logger = setup_logger(__name__)


class Vectorisation:
    def __init__(self):
        self.model_embeddings = HuggingFaceEmbeddings(
            model_name=os.getenv("DENSE_MODEL"),
        )
        self.splitter = SentenceTransformersTokenTextSplitter(
            model_name=os.getenv("DENSE_MODEL"),
        )

    def context_similarity_score(self, context: str, docs: list) -> float:
        if not context:  # Pass checking and gives max score
            return 1.0
        if not docs:  # Pass checking and gives min score
            return 0.0

        if isinstance(docs[0], Document):
            pages = [" ".join([doc.page_content for doc in docs])]
        elif isinstance(docs[0], Page):
            pages = [" ".join([doc.get_text() for doc in docs])]
        else:
            pages = []

        pages_embeddings = self.model_embeddings.embed_documents(pages)
        context_embeddings = self.model_embeddings.embed_documents([context])
        return cosine_similarity(context_embeddings, pages_embeddings)[0][0]

    def get_vector_data(self, chunks: List[Document]):
        dense_vectors = self.model_embeddings.embed_documents(
            [chunk.page_content for chunk in chunks]
        )
        return [
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
