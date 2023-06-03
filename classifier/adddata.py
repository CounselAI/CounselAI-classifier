import requests
import pandas as pd
from pprint import pprint
df = pd.read_csv('justice.csv')
df.columns = [x.capitalize() for x in df.columns]
df['Justia_url'] = ""
for idx in range(0, len(df['Href'])):
    res = requests.get(df['Href'][idx])
    url = res.json()["justia_url"] if res.json()["justia_url"] else ""
    pprint(url)
    df.loc[df['Href'] == df['Href'][idx], 'Justia_url'] = url
    df['Justia_url'][idx] = url

df.to_csv('justice_modified.csv', index=False)
