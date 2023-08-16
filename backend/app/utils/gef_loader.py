"""
Loads a GEFAnalyzer object from dotenv variables
"""

from dotenv import load_dotenv
import os
from gef_analyzr import GEFAnalyzer
from gef_analyzr.utils import get_ooba_llm, get_database_client


def gef_from_env():
    load_dotenv()

    llm = llm_from_env()
    qdrant = qdrant_from_env()

    return GEFAnalyzer(llm=llm, qdrant=qdrant)


def llm_from_env():
    url = os.getenv("LLM_URL")

    return get_ooba_llm(url)


def qdrant_from_env():
    params = {
        "url": os.getenv("QDRANT_URL"),
        "collection": os.getenv("COLLECTION"),
        "embedding_model": os.getenv("EMBEDDING_MODEL"),
    }

    return get_database_client(**params)
