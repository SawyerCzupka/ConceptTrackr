from gef_analyzr.search import ProjectQA
from gef_analyzr.utils import get_database_client, get_ooba_llm
from gef_analyzr import GEFAnalyzer

if __name__ == "__main__":
    database = get_database_client(
        "localhost:6333",
        collection="TEMP",
        embedding_model="multi-qa-mpnet-base-dot-v1",
    )

    gef = GEFAnalyzer(
        llm=get_ooba_llm(max_new_tokens=1500),
        qdrant=database,
    )

    question = "What are some major socioeconomic benefits of this Cambodia project?"

    response = gef.answerQuestionInProject(question, projectID=5318)
    print(f"\n\n---------- OUTPUT ----------\n\n")
    print(response["output_text"])
