import weaviate
from langchain_community.vectorstores.weaviate import Weaviate
from langchain.docstore.document import Document
from typing import List, Union
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader, UnstructuredExcelLoader
)
import logging
from django.conf import settings

from .engine import LLM
from utils.choices import FileType

logger = logging.getLogger(__name__)


class WeaviateService:

    def __init__(self, weaviate_url: str, index_name: str) -> None:
        """
        Initialize the WeaviateService with the specified Weaviate URL and index name.

        :param weaviate_url: The URL of the Weaviate instance.
        :param index_name: The name of the index in Weaviate.
        """
        self.weaviate_url = weaviate_url
        self.index_name = index_name
        self.weaviate_client = weaviate.Client(url=self.weaviate_url)
        self.weaviate_docstore = Weaviate(
            client=self.weaviate_client,
            index_name=self.index_name,
            text_key='text',
            embedding=LLM.embeddings,
            by_text=False
        )

    def create_documents_from_file(self, file_path: str, file_type: str, metadata: dict = None) -> List[Document]:
        """
        Create documents from a given file path and type.

        :param file_path: The path to the file.
        :param file_type: The type of the file (PDF, DOCX, CSV, XLSX, or Text).
        :param metadata: Optional metadata to add to each document.
        :return: A list of Document objects.
        """
        if metadata is None:
            metadata = {}

        loader = self.get_loader(file_path, file_type)
        docs = loader.load_and_split()

        for doc in docs:
            doc.metadata.update(metadata)

        return docs

    @staticmethod
    def get_loader(file_path: str, file_type: str) -> Union[
        TextLoader, PyPDFLoader, Docx2txtLoader, CSVLoader, UnstructuredExcelLoader]:
        """
        Get the appropriate loader for the given file type.

        :param file_path: The path to the file.
        :param file_type: The type of the file.
        :return: An instance of the appropriate loader.
        """
        if file_type == FileType.PDF:
            return PyPDFLoader(file_path)
        elif file_type == FileType.DOCX:
            return Docx2txtLoader(file_path)
        elif file_type == FileType.CSV:
            return CSVLoader(file_path)
        elif file_type == FileType.XLSX:
            return UnstructuredExcelLoader(file_path)
        else:
            return TextLoader(file_path)

    def add_documents(self, docs: List[Document]) -> None:
        """
        Add documents to the Weaviate instance.

        :param docs: A list of Document objects to be added.
        :return: None
        """
        return self.weaviate_docstore.add_documents(docs)

    def delete_documents(self, uuids: List[str]):
        for uuid in uuids:
            self.weaviate_client.data_object.delete(uuid=uuid)

    def similarity_search_with_score(self, query: str, k: int = 3, where_filter: dict = {}):
        if where_filter:
            return self.weaviate_docstore.similarity_search_with_score(query=query, k=k, where_filter=where_filter)
        return self.weaviate_docstore.similarity_search_with_score(query=query, k=k)
