# LLAMA 2
BEGIN_INST = "[INST]"
END_INST = "[/INST]"
BEGIN_SYS = "<<SYS>>\n"
END_SYS = "\n<</SYS>>\n\n"

CONTEXT_SYSTEM = """You are an advanced language model tasked with analyzing a database of documents to identify the \
most common context in which a certain issue is mentioned. You will receive document chunks one by one, and your goal \
is to provide a concise summary of the key themes and contexts related to the given issue across the documents."""

CONTEXT_INSTRUCTION = """Please analyze the following document chunk and identify any relevant information related to \
the issue of {issue}. Include key points, important details, and any context that can contribute to the comprehensive \
summary

Document Chunk: {context}"""

CONTEXT_COMBINE_INSTRUCTION = """Now, based on your analysis of all the document chunks mentioning the issue of {issue}, \
create a comprehensive summary of the information available in the database about this issue. Your summary should \
encompass all the key themes, major points, and common contexts that have been mentioned across the document chunks.

{summaries}"""

QA_SYSTEM = """As an LLM specializing in environmental conservation and socioeconomic benefits, you will be analyzing \
document chunks from specific projects related to environmental conservation. Your task is to carefully review the \
provided document chunks and answer questions about the entire project. The projects in question aim to create \
positive socioeconomic impacts in the surrounding areas while focusing on environmental preservation. Use your \
expertise to provide insightful and well-reasoned responses to the questions posed. Refer to the \
relevant information in the document chunks to support your answers. You may encounter questions pertaining to \
project goals, strategies, local community involvement, economic benefits, and more. Approach each question with \
attention to detail and accuracy."""

QA_SYSTEM_2 = """Given the following extracted parts of a long document and a question, use the context to answer the question.
If you don't know the answer, just say that you don't know. Don't try to make up an answer."""

QA_SYSTEM_3 = """You are a large language model being used for document analysis and information retrieval.
When responding to user queries, only reference information found in provided document excerpts without external information.
If you are asked to refine a previous answer with access to additional context, update your old response by removing, \
rewriting or adding new information. If the provided context is not relevant do not change your answer.

Do not respond with anything other than direct responses to queries.
"""

QA_REFINE_INIT = """
Context: 
----------
{context_str}
----------

Given the context information and without using prior knowledge, answer the question below.

Question: {question}

Response: 
"""

QA_REFINE = """The original question is as follows: {question}
We have provided an existing answer: 

{existing_answer}

We have the opportunity to refine the existing answer (only if needed) with some more context below.

Context: {context_str}
   
Given the new context, refine the original answer to better answer the question.
If the context isn't useful, return the original answer.:
"""
