import json

monuments_file = open('monuments-by-file.json', 'r')
monuments_data = json.load(monuments_file)

final_dict_list = []

for monument_file in monuments_data:
    for key in monument_file.keys():
        try:
            monument_file[key]["name"] = key
        except Exception as e:
            print(e)
            continue
        final_dict_list.append(monument_file[key])

json.dump(final_dict_list, open('monuments-uncompressed.json', 'w'), indent=4)