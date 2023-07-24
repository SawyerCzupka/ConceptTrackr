"""
This file contains all the logic for interacting with a Qdrant database and embedding new points into the database
"""
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer


class QdrantDatabase:
    def __init__(self, hostname='localhost', port=6333, collection='TEMP', embedding_model='all-mpnet-base-v2',
                 chunk_size=384, chunk_overlap=0, embedding_size=768):
        self._host = hostname
        self._port = port
        self.collection = collection
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_size = embedding_size

        self.client = QdrantClient(self._host, port=self._port)
        self.model = SentenceTransformer(embedding_model, device='cuda')
        self.splitter = self._get_splitter()

        self.nextID = 0

    def _get_splitter(self):
        return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.model.tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def _encode(self, text, **kwargs):
        return self.model.encode(text, **kwargs)

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.DOT)
        )

    def add_documents(self, documents: List[Document]):
        self.create_collection()

        chunks = self.chunk_documents(documents)
        embeds = self._encode([chunk.page_content for chunk in chunks], show_progress_bar=True)

        self.add_elements(chunks, embeds)

    def chunk_documents(self, documents) -> List[Document]:
        results = self.splitter.split_documents(documents)
        return results

    def _getID(self):
        ID = self.nextID
        self.nextID += 1
        return ID

    def add_elements(self, documents: List[Document], embedding_vectors):
        self.client.upsert(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=self._getID(),
                    payload={**document.metadata, **{'page_content': document.page_content}},
                    vector=embedding_vectors[i].tolist(),
                ) for i, document in enumerate(documents)
            ]
        )

    def search(self, text_query, **kwargs):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=self._encode(text_query).tolist(),
            **kwargs
        )

        return results
