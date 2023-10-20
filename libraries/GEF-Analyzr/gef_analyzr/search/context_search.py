from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient

from gef_analyzr.databases.qdrant import QdrantDatabase
from gef_analyzr.prompts.default_prompts import BEGIN_SYS, END_SYS, BEGIN_INST, END_INST, CONTEXT_SYSTEM, \
    CONTEXT_INSTRUCTION, CONTEXT_COMBINE_INSTRUCTION


class ContextSearcher:
    def __init__(self, llm, embedding_model, threshold=0.5):
        self.database = QdrantDatabase(embedding_model=embedding_model)

        qdrant = Qdrant(
            QdrantClient(host='localhost'),
            'TEMP',
            SentenceTransformerEmbeddings(model_name=embedding_model)
        )

        self.docsearch = qdrant.as_retriever()
        # self.ooba = TextGen(model_url='http://localhost:5000', max_new_tokens=1000)
        self._llm = llm

        templateStr = f"{BEGIN_INST} {BEGIN_SYS} {CONTEXT_SYSTEM} {END_SYS} {CONTEXT_INSTRUCTION} {END_INST}"
        self.question_prompt = PromptTemplate(template=templateStr, input_variables=['context', 'issue'])

        combine_template = f"{BEGIN_INST} {BEGIN_SYS} {CONTEXT_SYSTEM} {END_SYS} {CONTEXT_COMBINE_INSTRUCTION} {END_INST}"
        self.combine_prompt = PromptTemplate(template=combine_template, input_variables=['issue', 'summaries'])

        self.chain = self._create_map_reduce_chain()

    def _create_map_reduce_chain(self):
        chain = load_qa_chain(llm=self._llm, chain_type='map_reduce', question_prompt=self.question_prompt,
                              combine_prompt=self.combine_prompt)

        return chain

    @staticmethod
    def search_all_documents(threshold, chain='map_reduce'):
        """
        Finds the chunks of each document that are above the threshold and aggregates them together
        :param chain:
        :param threshold:
        :return:
        """

        pass

    def qa_search(self, query):
        docs = self.docsearch.get_relevant_documents(query)  # TODO replace with custom retrieval in database_interface

        return self.chain({'issue': query, 'input_documents': docs})
