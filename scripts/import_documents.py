import logging

from gef_analyzr.databases.qdrant import QdrantDatabase
from gef_analyzr.loaders.pdf_loader import DocumentLoader

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loader = DocumentLoader()
    database = QdrantDatabase(embedding_model='all-mpnet-base-v2', chunk_size=256, chunk_overlap=20)

    # Load desired files
    docs = loader.load_pdfs('../data/GEF/')

    # Insert to database
    database.add_documents(docs)
