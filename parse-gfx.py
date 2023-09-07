import pathlib
from pyparsing import *
import json
import os

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

nested_object << (Suppress('{') + Group(ZeroOrMore(property_group)) + Suppress('}'))

text_data = OneOrMore(property_group)
text_data.ignore('#' + rest_of_line)
###########################################################

# results = text_data.parse_string(
#     """
#     spriteType = {
# 		name = "GFX_religion_icon_strip"
# 		texturefile = "gfx/interface/icon_religion_small.dds"
# 		transparencecheck = yes
# 		noOfFrames = 60
# 	}
#     """
# )
# print(results)
# exit()

def gfx_parse(file_path):
    print(file_path)
    file_contents = open(file_path, 'r').read()
    try:
        results_lst = text_data.parse_string(file_contents)
    except ParseException as e:
        print(e.explain())
        return {}
    try:
        return convert_to_dictionary(results_lst.asList())
    except Exception as e:
        print(e.with_traceback())
        print(results_lst.asList())
        exit()

# converting to dictionary
def convert_to_dictionary(lst):
    output_dict = {}
    for item in lst:
        key = item[0]
        value = item[1]

        if isinstance(value, list):
            if isinstance(value[0], float):
                value = f"{value[0]} {value[1]} {value[2]}"
            else:
                value = convert_to_dictionary(value)

        # wild logic here  
        if not isinstance(output_dict, list):
            if key in output_dict.keys():
                output_dict = [output_dict, {key:value}]
            else:
                output_dict[key] = value 
        else:
            output_dict.append({key:value})
        
    return output_dict

gfx_paths = []
missing_interface = []

with open('monument-mod-manifest.json', 'r') as file:
    mod_manifest_file_data = json.load(file)

def recursive_monument_gfx_search(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            file = open(pathlib.WindowsPath(root).joinpath(file), 'r')
            for line in file:
                if 'GFX_great_project' in line:
                    gfx_paths.append(str(pathlib.WindowsPath(root).joinpath(file.name)))
                    break
        
        for directory_singular in dirs:
            recursive_monument_gfx_search(pathlib.WindowsPath.joinpath(dir, directory_singular))

for mod in mod_manifest_file_data['mods']:
    if pathlib.WindowsPath.exists(pathlib.WindowsPath(mod).joinpath('interface')):
        recursive_monument_gfx_search(pathlib.WindowsPath(mod).joinpath('interface'))
    else:
        missing_interface.append(mod)

gfx_paths_object = {
    "gfx_paths": gfx_paths
}

json.dump(gfx_paths_object, open('gfx-manifest.json', 'w'), indent=4)

gfx_dict_list = []

for path in gfx_paths:
    gfx_file_dict = gfx_parse(path)
    gfx_file_dict['filepath'] = path
    gfx_dict_list.append(gfx_file_dict)

json.dump(gfx_dict_list, open('gfx-compiled.json', 'w'), indent=4)