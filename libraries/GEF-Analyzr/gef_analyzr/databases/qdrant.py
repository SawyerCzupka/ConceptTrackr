"""
This file contains all the logic for interacting with a Qdrant database and embedding new points into the database
"""
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from gef_analyzr.utils import gef_metadata_from_filepath


class QdrantDatabase:
    def __init__(
        self,
        hostname="localhost",
        port=6333,
        collection="TEMP",
        embedding_model="all-mpnet-base-v2",
        chunk_size=384,
        chunk_overlap=0,
        embedding_size=768,
    ):
        self._host = hostname
        self._port = port
        self.collection = collection
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_size = embedding_size

        self.client = QdrantClient(self._host, port=self._port)
        self.model = SentenceTransformer(embedding_model, device="cuda")
        self.splitter = self._get_splitter()

        self.nextID = 0

    def _get_splitter(self):
        return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.model.tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def _encode(self, text, **kwargs):
        return self.model.encode(text, **kwargs)

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(
                size=self.vector_size, distance=models.Distance.DOT
            ),
        )

    def add_documents(self, documents: List[Document]):
        self.create_collection()

        chunks = self.chunk_documents(documents)
        embeds = self._encode(
            [chunk.page_content for chunk in chunks], show_progress_bar=True
        )

        self.add_elements(chunks, embeds)

    def chunk_documents(self, documents) -> List[Document]:
        results = self.splitter.split_documents(documents)
        return results

    def _getID(self):
        ID = self.nextID
        self.nextID += 1
        return ID

    def add_elements(self, documents: List[Document], embedding_vectors):
        def chunk_list(lst, chunk_size):
            """Divides a list into smaller chunks."""
            for i in range(0, len(lst), chunk_size):
                yield lst[i : i + chunk_size]

        chunk_size = 500
        total_docs = len(documents)
        total_chunks = (total_docs + chunk_size - 1) // chunk_size

        for chunk_idx, document_chunk in enumerate(chunk_list(documents, chunk_size)):
            start_idx = chunk_idx * chunk_size
            end_idx = min((chunk_idx + 1) * chunk_size, total_docs)

            chunk_vectors = embedding_vectors[start_idx:end_idx]
            chunk_documents = document_chunk

            points = [
                models.PointStruct(
                    id=self._getID(),
                    payload={
                        **document.metadata,
                        **{"page_content": document.page_content},
                        **gef_metadata_from_filepath(document.metadata["source"]),
                    },
                    vector=chunk_vectors[i].tolist(),
                )
                for i, document in enumerate(chunk_documents)
            ]

            self.client.upsert(collection_name=self.collection, points=points)

    def search(self, text_query, **kwargs):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=self._encode(text_query).tolist(),
            **kwargs
        )

        return results
