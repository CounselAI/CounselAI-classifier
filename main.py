from pydantic import BaseModel
from classifier import classifier
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
import dotenv
dotenv.load_dotenv(".env")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


class ID(BaseModel):
    ids: list


@app.get("/")
def read_root():
    return {"Hello": "World"}


class Query(BaseModel):
    query: str


@app.get("/cases/")
def read_item():
    return {"data": classifier.get_all()}


@app.post("/cases/compile/chatgpt")
def compile_item(data: ID):
    ids = []
    for id in data.ids:
        ids.append(int(id))
    return {"data": classifier.summarize_chatgpt(ids)}


@app.post("/cases/compile/nlp")
def compile_item(data: ID):
    ids = []
    for id in data.ids:
        ids.append(int(id))
    data = classifier.summarize_nlp(ids)
    return {"data": data}


@app.post("/cases/compile/ai21")
def compile_item(data: ID):
    ids = []
    for id in data.ids:
        ids.append(int(id))

    data = classifier.summarize_ai21(ids)
    return {'data': data}


@app.post("/cases/query")
def query_item(query: Query):
    print(query)
    return {"data": classifier.classify_query(query.query)}
