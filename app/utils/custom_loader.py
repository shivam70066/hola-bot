from langchain_community.document_loaders import PyPDFLoader,TextLoader,WebBaseLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from fastapi import HTTPException



class CustomLoader:
    
    def __init__(self, file_path, **kwargs):
        if file_path.endswith('csv'):
            self.loader = CSVLoader(file_path,**kwargs)
        elif file_path.endswith('.pdf'):
            self.loader = PyPDFLoader(file_path=file_path, **kwargs)
        elif file_path.endswith('.txt'):
            self.loader = TextLoader(file_path=file_path, **kwargs)
        elif file_path.startswith("http://") or file_path.startswith("https://"):
            self.loader = WebBaseLoader(file_path)
        else:
            raise HTTPException(status_code=400, detail="Invalid file format.")
            
    def load(self):
        return self.loader.load()