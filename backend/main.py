import pandas as pd
from fastapi import FastAPI, Body
from typing import Annotated, List

from backend.app.utils.gef_loader import gef_from_env
from backend.app.utils.response import df_to_csv_response
from gef_analyzr.prompts.gef_questions import SPREADSHEET_QUESTIONS

gef = gef_from_env()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/lorem")
def lorem():
    return {
        "output": "Nunc condimentum eros eget arcu rhoncus consequat. Phasellus molestie augue quam, sed cursus ante "
        "lacinia non. Aenean ultrices ex non lectus accumsan gravida. Fusce a libero vel velit ultricies "
        "iaculis. Maecenas lacinia sem sed accumsan interdum. In lacus tortor, facilisis suscipit vulputate "
        "at, dignissim eu lorem. Nunc nec semper eros. Proin sed mi nec sem volutpat vulputate et vitae eros. "
        "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. "
        "Praesent risus diam, gravida vel lectus ut, tincidunt feugiat purus. Mauris auctor turpis id "
        "mauris fringilla, eu porttitor velit viverra. Aenean sed enim sit amet ligula euismod posuere "
        "vitae in turpis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas luctus, "
        "purus vel imperdiet dictum, lectus elit placerat arcu, vitae pretium ipsum felis sit amet justo. "
        "Cras porta efficitur nulla."
    }


@app.post("/answerQuestionInProject")
def answerQuestion(question: Annotated[str, Body()], projectID: Annotated[int, Body()]):
    """
    Gives the model-generated answer to a question for a given project
    :param question: Question to be asked
    :param projectID: GEF project ID
    :return: answer string
    """
    return gef.answerQuestionInProject(question, projectID)


@app.post("/answerQuestionsInProject")
def answerQuestions(
    questions: Annotated[List[str], Body()], projectID: Annotated[int, Body()]
):
    """
    Gives the model-generated answers to many questions
    :param questions: Array of question strings
    :param projectID: GEF project ID
    :return: JSON
    """
    df = gef.answerQuestionsInProject(questions, projectID)

    return df.to_json()


@app.post("/generateSpreadsheet")
def generateSpreadsheet(projectID: Annotated[int, Body()]):
    """
    Generates a filled spreadsheet for a given project
    :param projectID: GEF project ID
    :return: csv file with responses
    """
    df = gef.answerQuestionsInProject(SPREADSHEET_QUESTIONS, projectID)

    return df_to_csv_response(df)
