import pandas as pd
import json
from .api import OPENAPI_KEY, AI21_KEY
from . import nlpsummarizer
# from api import OPENAPI_KEY
# import nlpsummarizer
from bs4 import BeautifulSoup
import openai
import requests
import ai21
openai.api_key = OPENAPI_KEY


def remove_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


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
    if data[-1] == '.':
        data = data[:-1]
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
    data = ". ".join(data)
    data = nlpsummarizer.generate_summary(data, 10)
    data = remove_html(data)
    return data


def summarize_ai21(ids: list):
    data = []

    ai21.api_key = AI21_KEY
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    for id in ids:
        data.append(df[df['Id'] == id]['Facts'].values[0])
    data = ". ".join(data)[:499]
    res = ai21.Paraphrase.execute(text=data,
                                  style="long")
    return res['suggestions'][0]['text']


if __name__ == "__main__":
    print(summarize_nlp([50606, 50644]))
