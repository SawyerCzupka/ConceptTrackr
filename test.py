import logging

from database_interface import QdrantDatabase
from document_loader import DocumentLoader

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loader = DocumentLoader()
    database = QdrantDatabase()

    # Load desired files
    # docs = loader.load_pdf('samples/05f0fb53-59d9-ed11-a7c7-000d3a5a70e0_PIF.pdf')
    docs = loader.load_pdfs('samples/')

    # Insert to database
    database.add_documents(docs)

    # print(database.search(
    #     "How much did the GEF spend on enabling environment for climate change adaptation in Djibouti?"))
