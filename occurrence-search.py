"""
This script aims to handle the logic for searching an already created database for occurrences of a single, predefined
issue.

This makes the following assumptions about the Vector Database:
- there is a metadata field 'documentID' that holds a unique ID for chunks from the same document.
"""

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


class OccurrenceSearcher:
    def __init__(self, issue: str, collection_name, database_host='localhost', database_port=6333, ):
        self.issue = issue

        self.client = QdrantClient(host=database_host, port=database_port)
        self.searchModel = SentenceTransformer('all-mpnet-base-v2')

    def getIssueEmbedding(self):
        return self.searchModel.encode(self.issue)

    def getUniqueDocumentOccurrences(self):
        query = self.getIssueEmbedding()

        # Search entire database for chunks that have a similarity value above the threshold
        self.client.search(
            collection_name='',
            query_vector=query,
            score_threshold=0.5
        )
