"""This file contains all the logic for loading different types of documents into a plaintext format that can be
indexed in a Qdrant database.

"""

import logging
import os
import uuid
from typing import List

from langchain.document_loaders import PDFPlumberLoader, PyPDFium2Loader


class DocumentLoader:
    def __init__(self, pdfLoader=PDFPlumberLoader):
        self.pdfLoader = pdfLoader
        self.id_gen = self._unique_id_generator()

    @staticmethod
    def _unique_id_generator():
        while True:
            yield str(uuid.uuid4())

    def load_pdf(self, path, documentID=None) -> List:
        docs = self.pdfLoader(path).load()

        if documentID:
            [doc.metadata.update({'documentID': documentID}) for doc in docs]

        return docs

    def load_pdfs(self, directory):
        file_docs = []
        for file in [file for file in os.listdir(directory) if file.endswith(".pdf")]:
            logging.info(f"File: '{directory + file}'")

            file_docs.extend(self.load_pdf(str(directory + file), documentID=next(self.id_gen)))

        return file_docs
