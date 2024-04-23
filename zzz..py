from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from configs.settings import settings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from custom_loader import CustomLoader
key= settings.OPEN_API_KEY

# loader = TextLoader("question.txt")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
# for item in docs:
#     print(item)

embeddings = OpenAIEmbeddings(openai_api_key=key)
weaviate_client = weaviate.connect_to_local(
    headers={"X-OpenAI-Api": key}
)

path = '/home/arcsinfotech/Desktop/hola bot/question.txt'  
custom_loader = CustomLoader(path)  
loaded_data = custom_loader.load()  

text_splitter = CharacterTextSplitter(
    chunk_size=200, chunk_overlap=200
)
chunks = text_splitter.split_documents(loaded_data)
print(chunks[0])

vector_store = WeaviateVectorStore(weaviate_client, "newDoc",text_key="page_content", embedding=embeddings)

id = vector_store.add_documents(chunks)
print(id)

# print(vector_store.similarity_search(query="i love to play", k=2))

print(vector_store.similarity_search_with_relevance_scores(query="where i want to visit?",k=2))

weaviate_client._connection.close()

# 3d253b4e-72d6-40fd-860c-37597a9cea11