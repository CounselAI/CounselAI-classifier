import pandas as pd
import json
from bs4 import BeautifulSoup
from .api import OPENAPI_KEY
from . import nlpsummarizer
import openai
import requests

openai.api_key = OPENAPI_KEY


def remove_html(text: str) -> str:
    bs = BeautifulSoup(text, 'html.parser')
    return bs.get_text()


def get_all():
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    return json.loads(df.to_json(orient='records'))


def classify_query(query: str):
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    issue_area = df['Issue_area'].unique().tolist()[1:]
    txt = f'''You are a lawyer, classify the following query: "{query}" into one of the following issue areas: {'  '.join(issue_area)} '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": txt},
        ]
    )
    data = ""
    for choice in response.choices:
        data += choice.message.content
    data.replace(".", "")
    print(data)
    return json.loads(df[df['Issue_area'] == data].to_json(orient='records'))


def summarize_chatgpt(ids: list):
    data = []
    references = []
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    for id in ids:
        url = requests.get(df.loc[df['Id'] == id]['Href'].values[0]).json()[
            "justia_url"]
        data.append(df[df['Id'] == id]['Facts'].values[0])
        references.append(
            url if url else df.loc[df['Id'] == id]['Href'].values[0])
    print(references)
    data = dict(zip(references, data))

    txt = f'''You are a lawyer, Summarize the following list of texts below into a single report. along with references : {data} write in points and link them to the reference '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": txt},
        ]
    )
    data = ""
    for choice in response.choices:
        data += choice.message.content
    return data


def summarize_nlp(ids: list):
    data = []
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    for id in ids:
        data.append(df[df['Id'] == id]['Facts'].values[0])
    data = remove_html(". ".join(data))
    data = nlpsummarizer.generate_summary(data, 10)
    return data


if __name__ == "__main__":
    print(summarize_nlp([50606, 50644]))
