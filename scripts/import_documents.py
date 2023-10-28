import logging
from dask import compute, distributed
from gef_analyzr.databases.qdrant import QdrantDatabase
from gef_analyzr.loaders.pdf_loader import DocumentLoader

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loader = DocumentLoader()

    # Dask setup
    client = distributed.Client()
    logging.info(f"Serving dask dashboard at {client.dashboard_link}")

    # Get PDF files generator
    pdf_files = loader.pdfs_generator("../data/dump/")
    logging.info(f"Found {len(pdf_files)} PDF files in the directory")

    # Parallelize the reading of PDFs
    docs_bag = db.from_sequence(pdf_files).map(loader.load_pdf)

    # Process and insert documents one by one
    database = QdrantDatabase(
        embedding_model="multi-qa-mpnet-base-dot-v1", chunk_size=512, chunk_overlap=20
    )

    for doc in docs_bag:
        database.process_and_add_documents(doc)
