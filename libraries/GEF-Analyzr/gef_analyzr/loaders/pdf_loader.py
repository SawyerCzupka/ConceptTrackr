import logging
import os
from typing import List
import dask.bag as db
from dask import compute, distributed

from langchain.document_loaders import PDFPlumberLoader, PyPDFium2Loader


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DocumentLoader:
    def __init__(self, pdfLoader=PDFPlumberLoader):
        self.pdfLoader = pdfLoader

    def load_pdf(self, path, documentID=None) -> List:
        try:
            docs = self.pdfLoader(path).load()
            logging.info(f"Successfully loaded {len(docs)} documents from {path}")
            if documentID:
                [doc.metadata.update({"documentID": documentID}) for doc in docs]
            return docs
        except Exception as e:
            logging.error(f"Error processing file '{path}' with loader: {e}")
            return []

    def load_pdfs(self, directory):
        pdf_files = [
            os.path.join(directory, file)
            for file in os.listdir(directory)
            if file.endswith(".pdf")
        ]

        logging.info(f"Found {len(pdf_files)} PDF files in {directory}")

        # Set up Dask client and start the dashboard
        client = distributed.Client()
        logging.info(f"Serving dask dashboard at {client.dashboard_link}")

        # Use dask.bag to create a bag of tasks
        bag = db.from_sequence(pdf_files).map(self.load_pdf)

        # Compute in parallel
        results = compute(bag)[0]

        # Flatten the list of lists into a single list
        file_docs = [item for sublist in results for item in sublist]

        logging.info(
            f"Completed processing all PDF files. Total documents loaded: {len(file_docs)}"
        )

        return file_docs
