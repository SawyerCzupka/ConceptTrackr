"""
This class serves as the main interface for this package. It consolidates all the features into an
easy-to-use class that takes care of all setup.
"""


class GEFAnalyzer:
    def __init__(self, qdrant, llm, embedding_model):
        self.database = qdrant
        self.llm = llm
        self.embedding_model = embedding_model

    def countOccurrences(self):
        pass

    def answerQuestion(self, question, projectID):
        # Must search only within the projectID
        pass

    def extractContext(self, issue):
        pass
