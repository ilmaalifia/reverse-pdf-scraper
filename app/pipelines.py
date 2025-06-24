import gc
import os

from app.milvus import Milvus
from app.utils import SCORING_PAGE_COUNT, setup_logger
from app.vectorisation import Vectorisation
from dotenv import load_dotenv

load_dotenv()

logger = setup_logger(__name__)


class ProcessingPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def open_spider(self, spider):
        self.context = getattr(spider, "context", None)
        self.vectorisation = Vectorisation()
        self.milvus = Milvus()

        # Dynamic threshold using z-score
        self.count = 0
        self.mean = 0.0
        self.M2 = 0.0
        self.zscore_threshold = float(os.getenv("ZSCORE_THRESHOLD", "0.5"))
        self.zscore_min_count = int(os.getenv("ZSCORE_MIN_COUNT", "30"))

    def close_spider(self, spider):
        gc.collect()

    def update(self, x):
        self.count += 1
        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.M2 += delta * delta2

    def std(self):
        if self.count < self.zscore_min_count:
            return None
        return (self.M2 / (self.count - 1)) ** 0.5

    def get_zscore(self, x):
        return (x - self.mean) / self.std() if self.std() else None

    def process_item(self, item, spider):
        url = item["url"]
        docs = item["docs"]
        total_size = item["total_size"]
        initial_threshold = item["initial_threshold"]

        # Duplicate checking
        if self.milvus.is_duplicate(url, total_size):
            return

        # Similarity score checking
        similarity_score = self.vectorisation.context_similarity_score(
            self.context, docs[:SCORING_PAGE_COUNT]
        )
        zscore = self.get_zscore(similarity_score)
        threshold = self.zscore_threshold if zscore else initial_threshold
        logger.info(
            f"Similarity score: {similarity_score} | z-score: {zscore} | Threshold {threshold}"
        )
        self.update(similarity_score)
        is_low_initial_similarity = not zscore and similarity_score < threshold
        is_low_zscore = zscore and zscore < threshold
        if is_low_initial_similarity or is_low_zscore:
            return

        try:
            chunks = self.vectorisation.splitter.split_documents(docs)
            vector_data = self.vectorisation.get_vector_data(chunks)
            inserted = self.milvus.insert_data(vector_data)
            if inserted.get("insert_count", 0) > 0:
                logger.info(
                    f"Successfully inserted {inserted['insert_count']} data of {url}"
                )
            del chunks, vector_data
        except Exception as e:
            logger.error(str(e))
        finally:
            return
