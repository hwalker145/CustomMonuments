import json
import pandas as pd

with open('monuments-uncompressed.json', 'r') as file:
    file_data = json.load(file)

df = pd.DataFrame(data=file_data, columns=file_data[0].keys())

df['tier_3_global_hash'] = df['tier_3'].apply(lambda d: hash(tuple(d['country_modifiers'].items())))
df['tier_3_area_hash'] = df['tier_3'].apply(lambda d: hash(tuple(d['area_modifier'].items())))
df['tier_3_province_hash'] = df['tier_3'].apply(lambda d: hash(tuple(d['province_modifiers'].items())))

df_compressed = df.drop_duplicates(subset=['name', 'tier_3_global_hash', 'tier_3_area_hash', 'tier_3_province_hash']).copy().reset_index(drop=True).fillna(0)
df_compressed = df_compressed[df_compressed['type'] == 'monument']
json.dump(df_compressed.to_dict(orient='records'), open('monuments-compressed.json', 'w'), indent=4)

df_compressed['Duplicates'] = df_compressed.groupby(['name'])['name'].transform('count')

iterable_rows = df_compressed[df_compressed['Duplicates'] > 1].sort_values('name').iterrows()
name = next(iterable_rows)[1]['name']

for i, duplicate_monument in iterable_rows:
    if name == duplicate_monument['name']:
        df_compressed.loc[i, 'name'] = df_compressed.loc[i, 'name'] + f"_{i}"
    else:
        name = duplicate_monument['name']

df_compressed['Duplicates'] = df_compressed.groupby(['name'])['name'].transform('count')

json.dump(df_compressed.to_dict(orient='records'), open('monuments-final-mended.json', 'w'), indent=4)