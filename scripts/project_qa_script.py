from gef_analyzr.search import ProjectQA
from gef_analyzr.utils import get_database_client, get_ooba_llm

if __name__ == "__main__":
    database = get_database_client(host='localhost', port=6333, collection='TEMP', embedding_model='multi-qa-mpnet-base-dot-v1')
    llm = get_ooba_llm(max_new_tokens=1500)
    qa = ProjectQA(database, llm, 'refine')

    question = "What are some major socioeconomic benefits of this Cambodia project?"

    response = qa.ask_question(question, projectID=5318)
    print(f"\n\n---------- OUTPUT ----------\n\n")
    print(response['output_text'])
