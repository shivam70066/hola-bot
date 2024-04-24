# from langchain_community.document_loaders import PyPDFLoader
# from configs.settings import settings

# # import getpass

# loader = PyPDFLoader("pdf/artificial_intelligence_tutorial.pdf")
# pages = loader.load_and_split()

# # print(pages[0].__str__)

# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

# faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings(api_key=settings.OPEN_API_KEY))
# docs = faiss_index.similarity_search("what is Philosophy of AI?", k=2)
# for doc in docs:
#     print(str(doc.metadata["page"]) + ":", doc.page_content[:300])
    
# from langchain_community.document_loaders import TextLoader

# text = 'pdf/hy.txt'
# loader = TextLoader(text)
# loader.load()
# print(loader.load())

"""[Document(page_content='The rise of generative models\n\nGenerative AI refers to deep-learning models that can take raw data—say, all of Wikipedia or the collected works of Rembrandt—and “learn” to generate statistically probable outputs when prompted. At a high level, generative models encode a simplified representation of their training data and draw from it to create a new work that’s similar, but not identical, to the original data.\nGenerative models have been used for years in statistics to analyze numerical data. The rise of deep learning, however, made it possible to extend them to images, speech, and other complex data types. Among the first class of AI models to achieve this cross-over feat were variational autoencoders, or VAEs, introduced in 2013. VAEs were the first deep-learning models to be widely used for generating realistic images and speech.', metadata={'source': '/content/textfile.txt'})]"""

# loader = TextLoader("/content/file.md")
# loader.load()

# from langchain_community.document_loaders import YoutubeLoader

# loader = YoutubeLoader.from_youtube_url(
#     "https://www.youtube.com/watch?v=75uBcITe0gU",
#     add_video_info = True,
#     language=["en","id"],
#     translation = 'hi'
# )
# print(loader.load())
# for document in loader.load():
#     print(document.page_content)


# from custom_loader import CustomLoader
# loader = None
# path = input("Enter Path: ")

# if path.endswith('.csv'):
#     loader = CustomLoader.load(path)

# pages = loader.loader()
# print(pages[0])

from app.utils.custom_loader import CustomLoader
import weaviate
import os
from dotenv import load_dotenv  
from langchain.text_splitter import CharacterTextSplitter
from weaviate.classes.config import Configure, Property, DataType
from configs.settings import settings
key= settings.OPEN_API_KEY
from langchain.vectorstores.weaviate import Weaviate

from langchain_openai import OpenAIEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore


path = '/home/arcsinfotech/Desktop/hola bot/question.txt'  
custom_loader = CustomLoader(path)  
loaded_data = custom_loader.load()  

text_splitter = CharacterTextSplitter(
    chunk_size=200, chunk_overlap=200
)

# Split the data into chunks
chunks = text_splitter.split_documents(loaded_data)
for doc in chunks:
    doc.metadata = {"src": "pdf/drylab.pdf"}
    
    
# print(chunks)


headers = {
    "X-OpenAI-Api-Key": key
} 

client = weaviate.Client(url="http://localhost:8080",additional_headers=headers)

if(client.schema.exists("newdoc2")):
    print("true")
embeddings = OpenAIEmbeddings(openai_api_key=key)
vectorstore = Weaviate(client, "newdoc2" , "page_content",embedding=embeddings)
        
assert client.is_live()  
if(client.is_live()):
    print("client is ready")
    
# print(client.schema.get())
# documents = vectorstore.as_retriever()

# # Print the content and metadata of each document
# for doc in documents:
#     print(f"Content: {doc.page_content}")
#     print(f"Metadata: {doc.metadata}")
# weaviate_client = weaviate.connect_to_local()
# db = WeaviateVectorStore.from_documents(chunks, embeddings, client=client)
# print(db)
# id= db.add_documents(chunks)
# print(len(id))
print(chunks)
for items in chunks:
    print(items.metadata.get['src'])
# ids = vectorstore.add_documents(chunks)
# print(ids)
# with client.batch as batch:
#     batch.configure(batch_size=50)
#     for doc in chunks:
#         batch.add_data_object(
#             {
#                 "page_content": doc.page_content,
#                 "src":"meta"
#             },
#             "newdoc2"
#     ) 
# print("----------------------------------------")
# print(vectorstore.schema())
# print(client.schema.get("newDoc"))
# print(vectorstore.similarity_search(query="what is my name?",k=2))
# docs = vectorstore.as_retriever().get_relevant_documents(query="pdf",k=1)
# for item in docs:
    # print(item.page_content)
    # print(item.metadata)
    
    # print("-"*22)
# print(docs)
# docs = vectorstore.similarity_search(query="+",k=1)
# print(docs)

# query = "What is Ai"
# docs = db.similarity_search(query,k=3)

# # Print the first 100 characters of each result
# for i, doc in enumerate(docs):
#     print(f"\nDocument {i+1}:")
#     print(doc.page_content)
#     print('-'*20)

# client = weaviate.Client("http://localhost:8080")
# vectorstore = Weaviate(client, "LangChain", "Document")

# query = "artificial"
# results = vectorstore.similarity_search(query)

# Print the results
# for result in results:
#     print(f"Score: {result.score}")
#     print(result.page_content)
#     print("-" * 20)

# Insert the chunks into the vector store
# print(vectorstore.add_documents(chunks))

# uuid = client.collections.create(
#     "MyData",
#     vectorizer_config=Configure.Vectorizer.text2vec_openai(),
#     properties=[  
#         Property(name="data", data_type=DataType.TEXT),
#         Property(name="metadata", data_type=DataType.TEXT),
#     ]
# )
# myData = client.collections.get("Document")
# articles.data.insert({
#     "title": "C++",
#     "body" : "learn c++"
# })

# for i, chunk in enumerate(chunks):
#     # print(f"Chunk {i+1}:")
#     # print(chunk.page_content)
#     # print(chunk.metadata)

#     # print("-" * 20)
#     id = myData.data.insert({
#     "data": chunk.page_content,
#     "metadat" : chunk.metadata
#     })
#     print(id)

# for item in myData.iterator():
#     print(item.uuid, item.properties)
    
# response = myData.query.near_text(
#     query="ttorial",
#     limit=1,
# )
# for o in response.objects:
#     print(o.properties.get('data'))
    
    
# print(myData)
# client.close()

vectorstore._client._connection.close()