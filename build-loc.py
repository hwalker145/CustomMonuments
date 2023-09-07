import json
import yaml
import pandas as pd

with open('localisation-by-file.json', 'r', encoding='utf-8') as file:
    loc_data = json.load(file)
with open('monuments-final-mended.json', 'r', encoding='utf-8') as file:
    monument_data = json.load(file)

monument_df = pd.DataFrame(monument_data)

# print(monument_df)
# exit()

results = monument_df[monument_df['name'].apply(lambda x: x.split('_')[-1].isnumeric())]
print(results[['name','filepath']])
exit()

yaml.safe_dump(loc_data, open('test03.yml', 'w', encoding='utf-8'), default_style='', indent=4, allow_unicode=True)