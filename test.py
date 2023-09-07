from pyparsing import *
import yaml
import pandas as pd

df = pd.DataFrame(
    [{
        "hello": 1,
        "hi": 2,
        "what's up": 3,
        "good day": 4,
        "hey": 5
    },
    {
        "hello": 0,
        "hi": 0,
        "what's up": 333,
        "good day": 21,
        "hey": 5
    },
    {
        "hello": 100,
        "hi": 200,
        "what's up": 300,
        "good day": 400,
        "hey": 500
    },
    {
        "hello": -1,
        "hi": -2,
        "what's up": -3,
        "good day": -4,
        "hey": -5
    }]
)

bob = df.iterrows()

for i, item in bob:
    print(item)
    if item['hi'] > 2:
        item['hi'] += 1

print(df)