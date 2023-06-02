from pydantic import BaseModel
from classifier import classifier
from fastapi import FastAPI
import dotenv
dotenv.load_dotenv(".env")
app = FastAPI()

class ID(BaseModel):
    ids:list
@app.get("/")
def read_root():
    return {"Hello": "World"}

class Query(BaseModel):
    query:str

@app.get("/cases/")
def read_item():
    return {"data":classifier.get_all()}

@app.post("/cases/compile")
def compile_item(data: ID):
    ids=[]
    for id in data.ids:
        ids.append(int(id))
    print(ids)
    return {"data":classifier.summarize(ids)}

@app.post("/cases/query")
def query_item(query: Query):
    return {"data":classifier.classify_query(query.query)}