from classifier import classifier
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/cases/")
def read_item():
    return classifier.read_all()