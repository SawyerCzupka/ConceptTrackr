# create-database.py
# This script is used for taking a database of plaintext documents and making a vector database out of them.

# Steps:
# 1. load data from existing database
# 2. go through documents, tokenize them, chunk them, and create embeddings.
# 3. add embeddings to vector database with metadata including the document ID it came from.

import logging
from typing import List

from langchain.document_loaders import PyPDFium2Loader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.DEBUG)

from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


def load_pdf_pdfium(path):
    return PyPDFium2Loader(path).load()


class DocumentProcessor:
    def __init__(self, embedding_model: str, chunk_size: int):
        # Parameters
        self.chunk_size = chunk_size
        self.model = SentenceTransformer(embedding_model, device='cuda')
        self.chunk_overlap = 0

        # Shared state
        self.documents = None

    def test_encoder(self):
        phrase = "Geology is the study of Earth and its components, including the study of rock formations. Petrology " \
                 "is the study of the character and origin of rocks. Mineralogy is the study of the mineral " \
                 "components that create rocks. The study of rocks and their components has contributed to the " \
                 "geological understanding of Earth's history, the archaeological understanding of human history, " \
                 "and the development of engineering and technology in human society."

        encoded = self.model.encode(phrase)
        print(f"Original: {phrase}\n\nEmbedding: {encoded}")

    def chunk_document(self, document):
        splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.model.tokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # chunks = splitter.split_text(text=document)

        chunks = splitter.split_documents(document)

        return chunks

    def create_embeddings(self, documents: List[Document]):
        return [self.model.encode(document.page_content) for document in documents]

    def process_document(self, path: str):
        """
        Adds the given document to a vector database after tokenizing, chunking and embedding.
        :param path: Path to the document (in this case pdf) to be
        :return: true if successful, false otherwise
        """

        loaded_pdf = load_pdf_pdfium(path)
        pdf_chunks = self.chunk_document(loaded_pdf)
        # embeddings = self.create_embeddings(pdf_chunks)

        return pdf_chunks


def add_documents_to_qdrant(documents: List[Document], embeddings, qdrant_host: str = 'localhost',
                            qdrant_port: int = 6333, collection: str = "TEMP"):
    url = f"{qdrant_host}:{qdrant_port}"
    url = r'http://localhost:6333/'
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=SentenceTransformerEmbeddings(model_name='all-mpnet-base-v2'),
        url=url,
        collection_name=collection
    )


class VectorDatabase:
    def __init__(self, qdrant_host, qdrant_port, collection_name, vector_size=768):
        self.client = QdrantClient('localhost', port=6333)
        self.collection = collection_name
        self.nextID = 0
        self.size = vector_size

        self.create_collection()

    def getId(self):
        self.nextID += 1
        return self.nextID - 1

    def create_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=self.size, distance=models.Distance.COSINE)
        )

    def add_elements(self, documents, embedding_vectors):
        self.client.upsert(
            collection_name=self.collection,
            points=[
                models.PointStruct(
                    id=self.getId(),
                    payload={
                        "chunk_content": doc.page_content,
                    },
                    vector=embedding_vector.tolist(),
                ) for doc, embedding_vector in zip(documents, embedding_vectors)
            ]
        )

    def add_documents(self, documents, embedding_generator: DocumentProcessor):
        embeds = embedding_generator.model.encode([document.page_content for document in documents],
                                                  show_progress_bar=True)

        self.add_elements(documents, embeds)


if __name__ == "__main__":
    pdf = PyPDFium2Loader('samples/Revised_EA.pdf').load()
    print(pdf)

    # creator = DocumentProcessor(embedding_model='all-mpnet-base-v2', chunk_size=384)
    # logging.debug("Creating vector database...")
    # db = VectorDatabase('localhost', 6333, 'Revised_EA', vector_size=768)
    # logging.debug("created vector database...")
    #
    # docs = creator.process_document('samples/Revised_EA.pdf')
    # logging.debug("processed document")
    #
    # db.add_documents(docs, creator)

    # db.add_documents(docs, creator)

    # db = VectorDatabase('localhost', '6333', 'TEST')
    # db.create_collection(3)
    # db.add_document(123)
