import pandas as pd

def read_all():
    df = pd.read_csv('justice.csv')
    return df[["name","term"]]