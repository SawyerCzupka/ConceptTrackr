import logging
import os
import uuid
from typing import List
from concurrent.futures import ProcessPoolExecutor, as_completed

from langchain.document_loaders import PDFPlumberLoader, PyPDFium2Loader


class DocumentLoader:
    def __init__(self, pdfLoader=PDFPlumberLoader):
        self.pdfLoader = pdfLoader
        # self.id_gen = self._unique_id_generator()

    # @staticmethod
    # def _unique_id_generator():
    #     while True:
    #         yield str(uuid.uuid4())

    def load_pdf(self, path, documentID=None) -> List:
        docs = self.pdfLoader(path).load()

        if documentID:
            [doc.metadata.update({'documentID': documentID}) for doc in docs]

        return docs

    def load_pdfs(self, directory):
        file_docs = []
        pdf_files = [file for file in os.listdir(directory) if file.endswith(".pdf")]
        total_files = len(pdf_files)

        with ProcessPoolExecutor() as executor:
            future_to_file = {executor.submit(self.load_pdf, str(directory + file), documentID=None): file for file in pdf_files}

            # Track the number of completed tasks
            completed_files = 0

            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    file_docs.extend(future.result())

                    # Increment the completed_files count and display progress
                    completed_files += 1
                    logging.info(f"Processed {completed_files}/{total_files} files")

                except Exception as e:
                    logging.error(f"Error loading file '{file}': {e}")

        return file_docs
