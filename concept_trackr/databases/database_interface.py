"""
This file contains all the logic for interacting with a Qdrant database and embedding new points into the database
"""
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from dotenv import load_dotenv
import os
import logging


class QdrantDatabase:
    def __init__(self, hostname='localhost', port=6333, collection='TEMP', embedding_model='all-mpnet-base-v2',
                 chunk_size=384, chunk_overlap=0):
        self.host = hostname
        self.port = port
        self.collection = collection

        # DOTENV
        # load_dotenv()
        # embedding_model = os.getenv("EMBEDDING_MODEL")

        self.client = QdrantClient(self.host, port=self.port)

        self.chunk_size = 128
        self.chunk_overlap = chunk_overlap
        self.vector_size = 768

        self.model = SentenceTransformer(embedding_model, device='cuda')
        self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/' + embedding_model)

        # self.splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        #     self.model.tokenizer,
        #     chunk_size=self.chunk_size,
        #     chunk_overlap=self.chunk_overlap
        # )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=384,
            chunk_overlap=100,
            length_function=self.len_func
        )

        # self.splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0,
        #                                                       model_name='sentence-transformers/' + embedding_model,
        #                                                       tokens_per_chunk=128)

        self.nextID = 0

    def len_func(self, text):
        length = len(self.tokenizer(text).get('input_ids'))
        return length

    def encode(self, text):
        return self.model.encode(text)

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.DOT)
        )

    def add_documents(self, documents: List[Document]):
        self.create_collection()

        chunks = self.chunk_documents(documents)
        embeds = self.model.encode([chunk.page_content for chunk in chunks], show_progress_bar=True)

        self.add_elements(chunks, embeds)

    def chunk_documents(self, documents) -> List[Document]:
        max_len = max([self.len_func(document.page_content) for document in documents])
        logging.info(f"Chunk_documents | Input Length: {len(documents)}, MaxLength: {max_len}")
        results = self.splitter.split_documents(documents)
        max_len = max([self.len_func(result.page_content) for result in results])
        logging.info(f"Chunk_documents | Output Length: {len(results)}, MaxLength: {max_len}")
        return results

    def getID(self):
        ID = self.nextID
        self.nextID += 1
        return ID

    def add_elements(self, documents: List[Document], embedding_vectors):
        documents[0].metadata.update()

        self.client.upsert(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=self.getID(),
                    payload={**documents[i].metadata, **{'page_content': documents[i].page_content}},
                    vector=embedding_vectors[i].tolist(),
                ) for i in range(len(documents))
            ]
        )

    def search(self, text_query, **kwargs):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=self.encode(text_query).tolist(),
            **kwargs
        )

        return results
