import pandas as pd
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from typing import Annotated, List
import celery_tasks
from celery.result import AsyncResult

from utils.response import df_to_csv_response


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test")
def test(test1: Annotated[str, Body(embed=True)]):
    return test1


@app.get("/task")
async def testTask():
    task = celery_tasks.add.delay()
    return JSONResponse({"task_id": task.id})


@app.get("/gefTest")
async def gefTest():
    task = celery_tasks.gefTest.delay()
    return JSONResponse({"task_id": task.id})


@app.post("/taskStatus/{task_id}")
async def taskStatus(task_id: str):
    print(f"Task ID: {task_id}")
    res = celery_tasks.celery_app.AsyncResult(task_id)

    if res.ready():
        return res.get()

    return res.status


@app.get("/tasks")
async def getTasks():
    # i = celery_tasks.celery_app.control.inspect()
    # return

    backend = celery_tasks.celery_app.backend.client.scan_iter
    task_results = []
    for key in backend.client.scan_iter("celery-task-meta-*"):
        task_id = str(key).split("celery-task-meta-", 1)[1].replace("'", "")
        task_results.append(celery_tasks.celery_app.AsyncResult(task_id))
    return task_results


@app.get("/lorem")
def lorem():
    return {
        "output": "Nunc condimentum eros eget arcu rhoncus consequat. Phasellus molestie augue quam, sed cursus ante "
                  "lacinia non. Aenean ultrices ex non lectus accumsan gravida. Fusce a libero vel velit ultricies "
                  "iaculis. Maecenas lacinia sem sed accumsan interdum. In lacus tortor, facilisis suscipit vulputate "
                  "at, dignissim eu lorem. Nunc nec semper eros. Proin sed mi nec sem volutpat vulputate et vitae eros."
                  " Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. "
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
    # return gef.answerQuestionInProject(question, projectID)
    pass


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
    # df = gef.answerQuestionsInProject(questions, projectID)

    # return df.to_json()
    pass


@app.post("/generateSpreadsheet")
def generateSpreadsheet(projectID: Annotated[int, Body(embed=True)]):
    """
    Generates a filled spreadsheet for a given project
    :param projectID: GEF project ID
    :return: csv file with responses
    """

    # df = gef.answerQuestionsInProject(SPREADSHEET_QUESTIONS, projectID)

    # return df_to_csv_response(df)
    pass


@app.get("/testFileDownload")
def testFileDownload():
    # Create a dictionary of data
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 22, 28],
        "City": ["New York", "San Francisco", "Los Angeles", "Chicago"],
    }

    # Create a DataFrame using the dictionary
    df = pd.DataFrame(data)

    return df_to_csv_response(df)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8111)