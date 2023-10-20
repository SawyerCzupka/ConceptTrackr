from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient


def get_database_client(
    url="localhost:6333", collection="TEMP", embedding_model="all-mpnet-base-v2"
):
    return Qdrant(
        QdrantClient(url=url),
        collection,
        SentenceTransformerEmbeddings(model_name=embedding_model)
    )
