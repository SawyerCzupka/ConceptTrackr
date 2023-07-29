from langchain.llms import TextGen

from gef_analyzr.search.context_search import ContextSearcher

if __name__ == "__main__":
    search = ContextSearcher(llm=TextGen(model_url='http://localhost:5000', max_new_tokens=1000), embedding_model='all-mpnet-base-v2')

    print(search.qa_search("water management"))
