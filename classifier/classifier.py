import pandas as pd
from bs4 import BeautifulSoup
import json
from pprint import pprint
from .secrets import OPENAPI_KEY
import openai 

openai.api_key = OPENAPI_KEY
def remove_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    txt=soup.get_text()
    txt=txt.replace('\n', '')
    txt=txt.replace('"', '')
    return txt

def get_all():
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    for idx in range (0,len(df['Facts'])):
        df['Facts'][idx] = remove_html(df['Facts'][idx])
    return json.loads(df.to_json(orient='records'))

def summarize(ids: list):
    data=[]
    for id in ids:
        df = pd.read_csv('justice.csv')
        df.columns = [x.capitalize() for x in df.columns]
        for idx in range (0,len(df['Facts'])):
            df['Facts'][idx] = remove_html(df['Facts'][idx])
        data.append(df[df['Id']==id]['Facts'].values[0])
    txt=f'''You are a lawyer, Summarize the following list of texts below into a single gist. : {'  '.join(data)} 
    in about 300 words divided into points'''
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "assistant", "content": txt},
        ]
    )
    data=""
    for choice in response.choices:
        data+=choice.message.content
    return data

def classify_query(query:str):
    df = pd.read_csv('justice.csv')
    df.columns = [x.capitalize() for x in df.columns]
    issue_area=df['Issue_area'].unique().tolist()[1:]
    txt=f'''You are a lawyer, classify the following query: "{query}" into one of the following issue areas: {'  '.join(issue_area)}'''
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "assistant", "content": txt},
        ]
    )
    data=""
    for choice in response.choices:
        data+=choice.message.content
    print(data)
    return json.loads(df[df['Issue_area']==data].to_json(orient='records'))
    #for idx in range (0,len(df['Facts'])):
    #    df['Facts'][idx] = remove_html(df['Facts'][idx])
    

if __name__=="__main__":
   pprint(classify_query("Murders after 2020")) 

