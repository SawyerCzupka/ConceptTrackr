# create-database.py
# This script is used for taking a database of plaintext documents and making a vector database out of them.

# Steps:
# 1. load data from existing database
# 2. go through documents, tokenize them, chunk them, and create embeddings.
# 3. add embeddings to vector database with metadata including the document ID it came from.

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, \
    SentenceTransformersTokenTextSplitter
from langchain.document_loaders import TextLoader
from transformers import AutoTokenizer
from typing import List


class DatabaseCreator:
    def __init__(self, embedding_model: str, chunk_size: int):
        # Parameters
        self.chunk_size = chunk_size
        self.model = SentenceTransformer(embedding_model)
        self.chunk_overlap = 20

        # Shared state
        self.documents = None
        self.fastTokenizer = AutoTokenizer.from_pretrained("sentence-transformers/gtr-t5-base")

    def test_encoder(self):
        phrase = "Geology is the study of Earth and its components, including the study of rock formations. Petrology " \
                 "is the study of the character and origin of rocks. Mineralogy is the study of the mineral " \
                 "components that create rocks. The study of rocks and their components has contributed to the " \
                 "geological understanding of Earth's history, the archaeological understanding of human history, " \
                 "and the development of engineering and technology in human society."

        encoded = self.model.encode(phrase)
        print(f"Original: {phrase}\n\nEmbedding: {encoded}")

    def load_documents(self, directory: str):
        # TODO find out how to get documents and then implement this
        self.documents = []
        pass

    def chunk_document(self, document: str):
        splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            self.fastTokenizer,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # chunks = splitter.split_text(text=document)

        chunks = splitter.split_documents(document)

        return chunks

    def add_document(self, document: str):
        """
        Adds the given document to a vector database after tokenizing, chunking and embedding.
        :param document: Plaintext representation of a document to be added to the vector database
        :return: true if successful, false otherwise
        """

        chunks = self.chunk_document(document)

        return chunks


def from_directory(path: str, database):
    """
    Takes text files in the given directory and adds them to an existing vector database.
    :param path:
    :return:
    """
    pass


if __name__ == "__main__":
    creator = DatabaseCreator(embedding_model='all-mpnet-base-v2', chunk_size=360)

    with open('samples/idk.txt', 'r') as file:
        contents = file.read()

    docs = TextLoader("samples/magnet.txt").load()

    chunks = creator.chunk_document(docs)

    print(len(chunks))
    for chunk in chunks:
        print(f"'{chunk}'\n")

    pass
