"""
This class serves as the main interface for this package. It consolidates all the features into an
easy-to-use class that takes care of all setup.
"""
from typing import List

from gef_analyzr.search import ProjectQA
import pandas as pd


class GEFAnalyzer:
    def __init__(self, qdrant, llm):
        self.database = qdrant
        self.llm = llm

        self._qa = None

    def answerQuestionInProject(self, question, projectID) -> str:
        # Must search only within the projectID
        if self._qa is None:
            self._qa = ProjectQA(self.database, self.llm, "refine")

        return self._qa.ask_question(question, projectID)

    def answerQuestionsInProject(
        self, questions: List[str], projectID: int
    ) -> pd.DataFrame:
        """
        Generates a pandas dataframe with responses to multiple questions

        :param questions: List of questions to be included in the dataframe
        :param projectID: Project to search through
        :return: dataframe with all questions and answers
        """

        df = pd.DataFrame(columns=["Question", "Response", "ProjectID"])

        for question in questions:
            response = self.answerQuestionInProject(question, projectID)
            # response = question
            newRow = {"Question": question, "Response": response, "ProjectID": projectID}

            df = df._append(newRow, ignore_index=True)

        return df
