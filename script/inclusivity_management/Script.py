import json
import pandas as pd


path='../../data.json'

with open(path) as f:
    dataset = json.load(f)

pos=[]
for tweet in dataset:
    df = pd.json_normalize(tweet['spacy'])
    pos.append(df)

print(pos)
