import logging

from concept_trackr.databases.database_interface import QdrantDatabase
from concept_trackr.loaders.pdf_loader import DocumentLoader
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    loader = DocumentLoader()
    database = QdrantDatabase(embedding_model=os.getenv('EMBEDDING_MODEL'))

    # Load desired files
    # docs = loader.load_pdf('data/05f0fb53-59d9-ed11-a7c7-000d3a5a70e0_PIF.pdf')
    docs = loader.load_pdfs('data/')

    # print(docs[0])

    # Insert to database
    database.add_documents(docs)

    # print(database.search(
    #     "How much did the GEF spend on enabling environment for climate change adaptation in Djibouti?"))
