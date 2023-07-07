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
                 chunk_size=384, chunk_overlap=0):
        self.host = hostname
        self.port = port
        self.collection = collection

        self.client = QdrantClient(self.host, port=self.port)

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_size = 768

        self.model = SentenceTransformer(embedding_model, device='cuda')
        self.splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.model.tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        self.nextID = 0

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE)
        )

    def add_documents(self, documents: List[Document]):
        self.create_collection()

        chunks = self.chunk_documents(documents)
        embeds = self.model.encode([document.page_content for document in documents], show_progress_bar=True)

        self.add_elements(chunks, embeds)

    def chunk_documents(self, documents):
        return self.splitter.split_documents(documents)

    def getID(self):
        ID = self.nextID
        self.nextID += 1
        return ID

    def add_elements(self, documents: List[Document], embedding_vectors):
        self.client.upsert(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=self.getID(),
                    payload=doc.metadata,
                    vector=embedding_vector.tolist(),
                ) for doc, embedding_vector in zip(documents, embedding_vectors)
            ]
        )

    def search(self, text_query):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=self.model.encode(text_query).tolist(),
            limit=4
        )

        return results
