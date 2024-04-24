from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from configs.settings import settings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from app.utils.custom_loader import CustomLoader
key= settings.OPEN_API_KEY

def deleteData(dataChunksIds:list):
    embeddings = OpenAIEmbeddings(openai_api_key=key)
        
    weaviate_client = weaviate.connect_to_local(
        headers={"X-OpenAI-Api": key}
    )
    vector_store = WeaviateVectorStore(weaviate_client, "newDoc",text_key="page_content", embedding=embeddings)
    vector_store.delete(dataChunksIds)
    print("done")