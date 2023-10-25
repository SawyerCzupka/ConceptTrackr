import logging

from gef_analyzr.databases.qdrant import QdrantDatabase
from gef_analyzr.loaders.pdf_loader import DocumentLoader

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loader = DocumentLoader()

    # Load desired files
    docs = loader.load_pdfs('../data/GEF/')

    # Insert to database
    database = QdrantDatabase(embedding_model='multi-qa-mpnet-base-dot-v1', chunk_size=512, chunk_overlap=20)
    database.add_documents(docs)
