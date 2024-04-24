from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from configs.settings import settings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from app.utils.custom_loader import CustomLoader
key= settings.OPEN_API_KEY

def ingestData(path:str):
    custom_loader = CustomLoader(path)
    loaded_data = custom_loader.load()
        
    embeddings = OpenAIEmbeddings(openai_api_key=key)
        
    weaviate_client = weaviate.connect_to_local(
        headers={"X-OpenAI-Api": key}
    )
  
    text_splitter = CharacterTextSplitter(
        chunk_size=200, chunk_overlap=200
    )
    chunks = text_splitter.split_documents(loaded_data)

    vector_store = WeaviateVectorStore(weaviate_client, "newDoc",text_key="page_content", embedding=embeddings)

    ids = vector_store.add_documents(chunks)

    # print(vector_store.similarity_search(query="i love to play", k=1))
    # print(vector_store.similarity_search_with_relevance_scores(query="where i want to visit?",k=2))

    weaviate_client._connection.close()
    return ids

