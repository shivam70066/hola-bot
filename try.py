from openai import OpenAI
from configs.settings import settings
key= settings.OPEN_API_KEY
client = OpenAI(api_key=key)

bot_response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "hello"}
  ]
)



print(bot_response.choices[0].message)

# def chat_with_gpt(prompt):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role":"user", "content": prompt}]
#     )
    
#     return response.choices[0].message.content.strip()

# if __name__ == "_-main__":
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["quit"]:
#             break
    
#         response = chat_with_gpt(user_input)
#         print("Chatbot: ", response)



from langchain.vectorstores import Weaviate
from weaviate import Client

client = Client('http://localhost:8080')
vector_store = Weaviate(client, "new", text_key="text")

data = [
    {"text": "This is the first document."},
    {"text": "This is the second document."},
    {"text": "This is the third document."}
]

ids = vector_store.add_texts(texts=[d["text"] for d in data])
print(ids)
