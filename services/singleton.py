from .weaviate_services import WeaviateService
from .engine import Chain
from django.conf import settings


class WeaviateServiceSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = WeaviateService(
                weaviate_url=settings.WEAVIATE_URL,
                index_name=settings.WEAVIATE_INDEX_NAME
            )
        return cls._instance

class ChainSingleton:
    _instance = None

    def __new__(cls, vectorstore):
        if cls._instance is None:
            cls._instance = Chain(vectorstore=vectorstore)
        return cls._instance



weaviate_service = WeaviateServiceSingleton()
chain_service = ChainSingleton(weaviate_service.weaviate_docstore)
