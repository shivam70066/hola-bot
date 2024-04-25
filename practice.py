import weaviate
from openai import OpenAI
import weaviate.classes.config as wc
from configs.settings import settings
key= settings.OPEN_API_KEY
import pandas as pd
import requests
from weaviate.util import generate_uuid5
import requests
from datetime import datetime, timezone
import json
from tqdm import tqdm
import os
import zipfile
from pathlib import Path
import base64
from weaviate.classes.query import MetadataQuery
from weaviate.classes.config import Configure, Property, DataType


headers = {
    "X-OpenAI-Api-Key": key
} 

client = weaviate.connect_to_local(headers=headers)
# client = weaviate.connect_to_local()
                                   
assert client.is_live()  # This will raise an exception if the client is not live
if(client.is_live()):
    print("client is ready")


# client.collections.create(
#     "newDoc",
#     vectorizer_config=Configure.Vectorizer.text2vec_openai(),
#     properties=[  
#         Property(name="page_content", data_type=DataType.TEXT),
#         Property(name="source", data_type=DataType.TEXT),
#     ]
# )


articles = client.collections.get("user23")


# uid = articles.data.insert({
#     "page_content": "Java",
#     "src" : "learn Java"
# })
# print(uid)
response = articles.query.fetch_object_by_id(uuid="f73bc2b8-0485-415f-b120-a0b27d9c4714")
print(response)  # Inspect the first object

# print(articles.data.delete_by_id('3d253b4e-72d6-40fd-860c-37597a9cea11'))


# for o in response.objects:
#     print(o)

# print(data_object.properties)
client.close()