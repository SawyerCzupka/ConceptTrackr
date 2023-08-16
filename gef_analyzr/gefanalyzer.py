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

    def countOccurrences(self):
        pass

    def answerQuestionInProject(self, question, projectID):
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
        :param projectID:
        :return:
        """

        df = pd.DataFrame(columns=["Question", "Response", "ProjectID"])

        for question in questions:
            response = self.answerQuestionInProject(question, projectID)
            df = df.append(
                {"Question": question, "Response": response, "ProjectID": projectID},
                ignore_index=True,
            )

        return df

    def extractContext(self, issue):
        pass
