from langchain_openai import OpenAIEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from configs.settings import settings


output_parser = StrOutputParser()
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPEN_API_KEY)


# def retrieval_chain(question:str,userID:int,chat_history:any):
#     weaviate_client = weaviate.connect_to_local(
#         headers={"X-OpenAI-Api": settings.OPEN_API_KEY}
#     )
#     llm = ChatOpenAI(api_key=settings.OPEN_API_KEY)
#     prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

#         <context>
#         {context}
#         </context>

#         Question: {input}""")
#     document_chain = create_stuff_documents_chain(llm, prompt)
#     vector_store = WeaviateVectorStore(weaviate_client, "user"+str(userID) , text_key="page_content", embedding=embeddings)
#     retriever = vector_store.as_retriever(search_kwargs={"k": 5})
#     retrieval_chain = create_retrieval_chain(retriever, document_chain)
#     response = retrieval_chain.invoke({"input": question})
#     weaviate_client.close()
#     return response




def retrieval_chain(question:str,userID:int,chat_history:any):
    weaviate_client = weaviate.connect_to_local(
        headers={"X-OpenAI-Api": settings.OPEN_API_KEY}
    )
    llm = ChatOpenAI(api_key=settings.OPEN_API_KEY)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context and history and if user asked about any other thing tell them you don't know:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    document_chain = create_stuff_documents_chain(llm, prompt)
    vector_store = WeaviateVectorStore(weaviate_client, "user"+str(userID) , text_key="page_content", embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    context = vector_store.similarity_search(query=question,k=5)
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
    response= retrieval_chain.invoke({
        "chat_history": chat_history,
        "input": question,
        "context": context
    })
    weaviate_client.close()
    return response

    
# retrieval_chain()