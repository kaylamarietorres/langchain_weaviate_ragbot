import logging
from .singleton import chain_service, weaviate_service

LOGGER = logging.getLogger(__name__)

class Chat:

    @staticmethod
    def chat(query, chat_history):
        LOGGER.info(f"Received query: {query}")
        relevant_chunks = weaviate_service.similarity_search_with_score(query=query, k=3)
        context = "\n".join([chunk[0].page_content for chunk in relevant_chunks])
        chat_history_str = ("\n".join([f"Human: {msg['query']}\nAI: {msg['response']}" for msg in chat_history]))
        response = chain_service.chain_rag.invoke({"context": context, "question": query, "chat_history": chat_history_str})
        LOGGER.info(f"Response: {response}")
        return response