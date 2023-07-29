from gef_analyzr.search import ProjectQA
from gef_analyzr.utils import get_database_client, get_ooba_llm

if __name__ == "__main__":
    database = get_database_client(host='localhost', port=6333, collection='TEMP', embedding_model='all-mpnet-base-v2')
    llm = get_ooba_llm(max_new_tokens=1000)
    qa = ProjectQA(database, llm, 'refine')

    question = "What populations might be impacted by this project?"

    response = qa.ask_question(question, projectID=5362)

    print(response['output_text'])
