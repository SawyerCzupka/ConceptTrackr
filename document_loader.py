"""This file contains all the logic for loading different types of documents into a plaintext format that can be
indexed in a Qdrant database.

"""

import logging
import os
import uuid
from typing import List

from langchain.document_loaders import PDFPlumberLoader


class DocumentLoader:
    def __init__(self, pdfLoader=PDFPlumberLoader):  # TODO address duplicates produced by PDFPlumber
        self.pdfLoader = pdfLoader
        self.id_gen = self.unique_id_generator()

    def unique_id_generator(self):
        while True:
            yield str(uuid.uuid4())

    def load_pdf(self, path, documentID=None) -> List:
        docs = self.pdfLoader(path).load()

        if documentID:
            [doc.metadata.update({'documentID': documentID, 'content': doc.page_content}) for doc in docs]

        return docs

    def load_pdfs(self, directory):
        docs = []
        for file in [file for file in os.listdir(directory) if file.endswith(".pdf")]:
            logging.debug(f"File: '{directory + file}'")

            docs.extend(self.load_pdf(str(directory + file), documentID=next(self.id_gen)))

        return docs
