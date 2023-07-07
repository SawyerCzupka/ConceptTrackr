"""
This script aims to handle the logic for searching an already created database for occurrences of a single, predefined
issue.

This makes the following assumptions about the Vector Database:
- there is a metadata field 'documentID' that holds a unique ID for chunks from the same document.
"""
import os

from database_interface import QdrantDatabase
from dotenv import load_dotenv
from qdrant_client import models


class OccurrenceSearcher:
    def __init__(self, issue: str, threshold=0.5):
        load_dotenv()
        self.query = issue
        self.database = QdrantDatabase(embedding_model=os.getenv("EMBEDDING_MODEL"))
        self.threshold = threshold

    def getUniqueDocumentOccurrences(self):
        # Search entire database for chunks that have a similarity value above the threshold
        results = self.database.search(
            self.query,
            # score_threshold=None,  # self.threshold,  # TODO find optimal value
            with_payload=models.PayloadSelectorInclude(
                include=['page_content', 'page', 'file_path']
            ),
            limit=0
        )

        # print(f"First Result: '{results[0]}'")

        return results
