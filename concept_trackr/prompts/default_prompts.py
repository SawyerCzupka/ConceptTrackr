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

COMBINE_INSTRUCTION = """Now, based on your analysis of all the document chunks mentioning the issue of {issue}, \
create a comprehensive summary of the information available in the database about this issue. Your summary should \
encompass all the key themes, major points, and common contexts that have been mentioned across the document chunks.

{summaries}"""