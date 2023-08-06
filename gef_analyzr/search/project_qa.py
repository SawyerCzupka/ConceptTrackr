"""
This file contains all the logic for using the vectorized database to answer project specific questions based on their
documents. This is intended to be used to programmatically fill out project analysis spreadsheets to save time.
"""

from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant, VectorStore
from langchain.llms.base import LLM
from langchain.chains.question_answering import load_qa_chain
from gef_analyzr.prompts import QA_SYSTEM, QA_REFINE, QA_REFINE_INIT, BEGIN_SYS, BEGIN_INST, END_SYS, END_INST
from langchain import PromptTemplate
from qdrant_client.http import models
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain


class ProjectQA:
    def __init__(self, vectorstore: VectorStore, llm: LLM, chain_type):
        self._database = vectorstore
        self._llm = llm

        chain_mapping = {
            'refine': self._create_refine_chain
        }

        self._qa: BaseCombineDocumentsChain = chain_mapping[chain_type]()

    def ask_question(self, question, projectID):
        docs = self._get_documents_from_project(question, projectID, k=5)

        return self._qa({'input_documents': docs, 'question': question}, return_only_outputs=True)

    def _get_documents_from_project(self, query: str, projectID: int, search_type='similarity', **kwargs):
        search_filter = models.FieldCondition(
            key='projectID',
            match=models.MatchValue(value=f'{projectID}')
        )

        return self._database.search(query=query, search_type=search_type, filter=search_filter, **kwargs)

    def _create_refine_chain(self):
        question_tmpl = f"{BEGIN_INST} {BEGIN_SYS} {QA_SYSTEM} {END_SYS} {QA_REFINE_INIT} {END_INST}"
        question_prompt = PromptTemplate(
            input_variables=['question', 'context_str'],
            template=question_tmpl
        )

        refine_tmpl = f"{BEGIN_INST} {BEGIN_SYS} {QA_SYSTEM} {END_SYS} {QA_REFINE} {END_INST}"
        refine_prompt = PromptTemplate(
            input_variables=["question", "existing_answer", "context_str"],
            template=refine_tmpl
        )

        return load_qa_chain(
            self._llm,
            chain_type='refine',
            question_prompt=question_prompt,
            refine_prompt=refine_prompt
        )
