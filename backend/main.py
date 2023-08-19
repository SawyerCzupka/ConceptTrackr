import pandas as pd
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from typing import Annotated, List
import io

from backend.app.utils.gef_loader import gef_from_env

# import gef_from
# from app.utils.gef_loader import gef_from_env

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
    return gef.answerQuestionInProject(question, projectID)


@app.post("/answerQuestionsInProject")
def answerQuestions(
    questions: Annotated[List[str], Body()], projectID: Annotated[int, Body()]
):
    df = gef.answerQuestionsInProject(questions, projectID)
    # data = {
    #     "Question": ["What is your name?", "How are you?"],
    #     "Response": [
    #         "My name is Alice.",
    #         "I'm doing well, thank you!",
    #     ],
    #     "ProjectID": [123, 123],
    # }
    #
    # df = pd.DataFrame(data)

    csv_content = df.to_csv(index=False)
    csv_bytes = io.BytesIO(csv_content.encode())

    return StreamingResponse(
        csv_bytes,
        headers={"Content-Disposition": "attachment; filename=exported_data.csv"},
        media_type="text/csv",
    )
