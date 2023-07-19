from dotenv import load_dotenv
from database_interface import QdrantDatabase
import os
import langchain
from langchain import PromptTemplate, LLMChain
from langchain.llms import TextGen
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA


class ContextSearcher:
    def __init__(self, issue: str, threshold=0.5):
        load_dotenv()
        self.query = issue
        self.database = QdrantDatabase(embedding_model=os.getenv("EMBEDDING_MODEL"))

        qdrant = Qdrant(
            QdrantClient(host='localhost'),
            'TEMP',
            SentenceTransformerEmbeddings('sentence-transformers/all-mpnet-base-v2')
        )

        docsearch = qdrant.as_retriever()
        ooba = TextGen(model_url='http://localhost:5000')

        self.qa = RetrievalQA.from_chain_type(llm=ooba, chain_type='map_reduce', retriever=docsearch)

    def _create_llm(self, model_ur='http://localhost:5000'):
        return TextGen(model_url=model_ur)

    def embed(self, text):
        pass

    @staticmethod
    def search_all_documents(threshold):
        """
        Finds the chunks of each document that are above the threshold and aggregates them together
        :param threshold:
        :return:
        """

        pass
