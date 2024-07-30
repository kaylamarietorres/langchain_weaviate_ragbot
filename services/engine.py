from django.conf import settings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain.chains.llm import LLMChain
from langchain_community.llms import OpenAI
from langchain.callbacks import StdOutCallbackHandler


class LLM:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")


class Chain:
    def __init__(self, vectorstore: VectorStore) -> None:
        # Get retriever from vectorstore
        self.retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
        # RAG prompt
        template = """Answer the question based on the following context:
        {context}
        ```
        The conversation history:
        {chat_history}
        ```
        Question: 
        {question}
        ```

        use your knowledge to answer the question only if no answer is found in the context.
        """
        prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"], template=template
        )
        openai = OpenAI()
        self.chain_rag = LLMChain(llm=openai, prompt=prompt)
