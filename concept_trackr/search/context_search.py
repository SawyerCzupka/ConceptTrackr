from dotenv import load_dotenv
from concept_trackr.databases.database_interface import QdrantDatabase
import os
from langchain.llms import TextGen
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain import PromptTemplate


class ContextSearcher:
    def __init__(self, threshold=0.5):
        load_dotenv()
        self.database = QdrantDatabase(embedding_model=os.getenv("EMBEDDING_MODEL"))

        qdrant = Qdrant(
            QdrantClient(host='localhost'),
            'TEMP',
            SentenceTransformerEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
        )

        self.docsearch = qdrant.as_retriever()
        self.ooba = TextGen(model_url='http://localhost:5000', max_new_tokens=1000)

        b_inst = "[INST]"
        e_inst = "[/INST]"
        b_sys = "<<SYS>>\n"
        e_sys = "\n<</SYS>>\n\n"

        context_sys = "You are an advanced language model tasked with analyzing a database of documents to identify " \
                      "the most common context in which a certain issue is mentioned. You will receive document " \
                      "chunks one by one, and your goal is to provide a concise summary of the key themes and " \
                      "contexts related to the given issue across the documents."

        context_inst = """Please analyze the following document chunk and identify any relevant information related 
        to the issue of {issue}. Include key points, important details, and any context that can contribute to the comprehensive summary

Document Chunk: {context}"""

        templateStr = f"{b_sys} {context_sys} {e_sys} {b_inst} {context_inst} {e_inst}"
        self.question_prompt = PromptTemplate(template=templateStr, input_variables=['context', 'issue'])
        combine_inst = """Now, based on your analysis of all the document chunks mentioning the issue of {issue}, create a comprehensive summary of the information available in the database about this issue. Your summary should encompass all the key themes, major points, and common contexts that have been mentioned across the document chunks.

{summaries}"""

        combine_template = f"{b_sys} {context_sys} {e_sys} {b_inst} {combine_inst} {e_inst}"
        self.combine_prompt = PromptTemplate(template=combine_template, input_variables=['issue', 'summaries'])
        # context_chain = load_qa_chain(llm=ooba, chain_type="stuff", prompt=context_prompt)

        # self.llama2template = PromptTemplate(template=templateStr, input_variables=["query"])

        self.chain = self._create_map_reduce_chain()

        # chain_type_kwargs = {
        #     "question_prompt": context_prompt,
        #     "combine_prompt": combine_prompt,
        #
        # }
        #
        # self.qa = RetrievalQA.from_chain_type(llm=ooba, chain_type='map_reduce', retriever=docsearch,
        #                                       chain_type_kwargs=chain_type_kwargs)

    def _create_map_reduce_chain(self):
        chain = load_qa_chain(llm=self.ooba, chain_type='map_reduce', question_prompt=self.question_prompt,
                              combine_prompt=self.combine_prompt)

        return chain

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

    def qa_search(self, query):
        docs = self.docsearch.get_relevant_documents(query)

        return self.chain({'issue': query, 'input_documents': docs})
