import json
import pandas
import pathlib
from pyparsing import *

file_manifest_path = 'file-manifest.json'
file_manifest_data = json.load(open(file_manifest_path, 'r'))

file_paths = file_manifest_data['files']

monuments_df_columns = [
    "Name",
    "Province",
    "Localization (English)",
    "Graphics path",
    "Effects",
    "Movable",
    "Move time",
    "Time to build",
    "Cost to build",
    "Type",
    "Date built",
    "On destroyed",
    "On built",
    "Starting tier",
    "Tier 0",
    "Tier 1",
    "Tier 2",
    "Tier 3"
]
monuments_df = pandas.DataFrame(columns=monuments_df_columns)

monuments_files_parsed_list = []
failed_files_list = []

# pyparsing definitions ##########################
date_format = Combine(Optional('-') + Word(nums) + "." + Word(nums) + "." + Word(nums))
unquoted_string = Word(alphanums + "./_-?")
quoted_string = (dblQuotedString | sglQuotedString).setParseAction(remove_quotes)
decimal_number = Regex(r"[+-]?\d+\.\d*").setParseAction(lambda x: float(x[0]))
integer_number = Word(nums).setParseAction(lambda x: int(x[0]))
color = Suppress('{') + Group(decimal_number + decimal_number + decimal_number) + Suppress('}')

nested_object = Forward()
property_value = date_format | decimal_number | integer_number | unquoted_string | quoted_string | color
property_group = Group(unquoted_string + Suppress("=") + (property_value | nested_object))

nested_object << Group(Suppress('{') + ZeroOrMore(property_group) + Suppress('}'))

text_data = OneOrMore(property_group)
text_data.ignore('#' + rest_of_line)
###########################################################

# result = text_data.parse_string(
#     """
#     john = { 
#     # sdaosdad {}{}{}
#         james = { jimmy = { hello = {hi = 30.7} } }
#         jim = 3.00033
#     }
# """
# )
# print(result)
# exit()

def monument_parse(file_path: pathlib.Path):
    print(file_path)
    file_contents = open(file_path, 'r').read()
    try:
        results_lst = text_data.parse_string(file_contents)
    except ParseException as e:
        print(e)
        return {}
    return convert_to_dictionary(results_lst.asList())

# converting to dictionary
def convert_to_dictionary(lst):
    output_list = []
    output_dict = {}
    for item in lst:
        key = item[0]
        value = item[1]

        if isinstance(value, list):
            value = convert_to_dictionary(value)
            
        output_dict[key] = value
        
    output_list.append(output_dict)
    if len(output_list) == 1:
        return output_list[0]
    else:
        return output_list

for filepath_singular in file_paths:
    parsed_monument_file = monument_parse(pathlib.WindowsPath(filepath_singular))

    if not parsed_monument_file:
        continue

    for monument in parsed_monument_file.keys():
        parsed_monument_file[monument]['filepath'] = str(pathlib.WindowsPath(filepath_singular))

    monuments_files_parsed_list.append(parsed_monument_file)

json.dump(monuments_files_parsed_list, open('monuments-by-file.json', 'w'), indent=4)