from pyparsing import *
import json
import os
import pathlib
import yaml

# find the loc files for the monuments
with open('monument-mod-manifest.json', 'r') as file:
    mod_manifest_data = json.load(file)

loc_paths = []
missing_loc = []

# YAML parsing ###############
comment = '#' + rest_of_line

unquoted_string = Word(alphanums + ".,();&![]/_-?=:%+'\\" + '\n' + 
                       pyparsing_unicode.Latin1.alphas + 
                       pyparsing_unicode.LatinA.alphas + 
                       pyparsing_unicode.LatinB.alphas + "\u00a7\u2013")

key = Word(alphanums + "._-")

nested_string = Suppress('"') + Combine(ZeroOrMore(unquoted_string | dbl_quoted_string), adjacent=False, joinString=' ') + Suppress('"')
#nested_string.setParseAction(remove_quotes)

property = Forward()
value = (nested_string | Group(ZeroOrMore(property)) | comment)
property << Group(key + Suppress(':') + Suppress(Optional(Word(nums))) + value)

yaml_data = OneOrMore(property)
yaml_data.ignore(comment)
##############################

def convert_to_dictionary(lst):
    output_dict = {}
    for item in lst:
        key = item[0]
        value = item[1]
        if isinstance(value, list):
            value = convert_to_dictionary(value)
        output_dict[key] = value
    return output_dict

# string = \
#  """
#  l_english:
 
#  #Made for Flavor Universalis by Big Boss#
 
#  FU_Monument_Events.1.t: "The Brandenburg Gate"
#  FU_Monument_Events.1.d: "The Brandenburg Gate is an 18th-century neoclassical monument in Berlin, built on the orders of Prussian king [Root.Monarch.GetName] to celebrate the brilliance and affluence of our people. One of the best-known landmarks of Germany, it was built on the site of a former city gate that marked the start of the road from Berlin to the town of Brandenburg an der Havel, which used to be capital of the Margraviate of Brandenburg. \n\nThe new gate was commissioned by [Root.Monarch.GetName] to represent peace and was originally named the Peace Gate. The gate consists of twelve Doric columns, six to each side, forming five passageways. Citizens were originally allowed to use only the outermost two on each side. Its design is based on the Propylaea, the gateway to the Acropolis in Athens, Greece, and is consistent with Berlin's history of architectural classicism (first, Baroque, and then neo-Palladian). The gate was the first element of a "new Athens on the River Spree" by local famed architects. Atop the gate is a sculpture by Johann Gottfried 'Schadow of a Quadriga' - a chariot drawn by four horses - driven by Victoria, the Roman goddess of victory." 
#  FU_Monument_Events.1.a: "A wondrous display of diplomatic prestige & elegance!"
 
#  FU_Monument_Events.3.t: "The Glory of Arts & Culture - Porcelain Tower"
#  FU_Monument_Events.3.d: "Erected during the late Yongle Emperor's reign, the Porcelain Tower is a magnificent display of splendor and affluence, the continuous prosperity of our people. The recent expansion of the tower's facilities have led to the complex attracting the most amazing great minds across the Chinese subcontinent and beyond. This influx of thought and people of the arts will surely assist the innovation of new technologies and the acceptance of all people under the roof of our gigantic domain. Truly, the beginning of a golden era for the literary and cultural arts!"
#  FU_Monument_Events.3.a: "A sign of heavenly favor!"
 
#  FU_Monument_Events.4.t: "Globe Theatre in London"
#  FU_Monument_Events.4.d: "Built in 1599 AD on Maiden Lane in London by the Lord Chamberlain's Men, the theatrical company of which William Shakespeare was a shareholder, the Globe Theatre incorporated a number of design innovations. In 1613 the Globe burned to the ground after the thatched roof was set alight by cannonfire during a production of Henry VIII; it was rebuilt on the same site in 1614 and continued in operation until closed by the Puritans in 1642. Although its exact dimensions are unrecorded, it is known that the Globe Theatre was a three-story, circular, open-air amphitheater roughly 30 meters (100 feet) in diameter and able to seat about 300 spectators. The stage was 13 meters (43 feet) wide, 8 meters (27 feet) deep and raised five feet off the ground, allowing for trap doors."
#  FU_Monument_Events.4.a: "All the world's a stage!"
#  """


# path = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\236850\\2164202838\\localisation\\FU_Monument_Events_l_english.yml"
# path = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\236850\\2471249210\\localisation\\monumenta_italiano_l_english.yml"
# print(open(path, 'r', encoding='utf-8').read().lstrip('\ufeff'))
# exit()

# result = yaml_data.parse_string(open(path, 'r', encoding='utf-8').read().lstrip('\ufeff'))
# print(result.asList())
# final_dict = convert_to_dictionary(result.asList())
# print(final_dict)
# exit()
# json.dump(final_dict, open('test04.json', 'w', encoding='utf-8'), indent=4)
# exit()

def recursive_monument_loc_search(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if 'monument' in str(file).lower() and 'english' in str(file).lower():
                loc_paths.append(str(pathlib.WindowsPath(root).joinpath(file)))
        
        for directory_singular in dirs:
            recursive_monument_loc_search(pathlib.WindowsPath.joinpath(dir, directory_singular))

for mod in mod_manifest_data['mods']:
    if pathlib.WindowsPath.exists(pathlib.WindowsPath(mod).joinpath('localisation')):
        recursive_monument_loc_search(pathlib.WindowsPath(mod).joinpath('localisation'))
    else:
        missing_loc.append(mod)

json.dump({"paths": loc_paths}, open('loc-manifest.json', 'w'), indent=4)

dict_list = []

for file_path in loc_paths:
    # print(file_path)
    # exit()
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        file_contents = file_contents.lstrip('\ufeff')
        # print(file_contents)
        # print(parsed_list.asList())
        # print(convert_to_dictionary(parsed_list.asList()))
        # yaml.safe_dump(convert_to_dictionary(parsed_list.asList()), open('test05.yml', 'w', encoding='utf-8'), allow_unicode=True)
        # exit()
    try:
        parsed_loc_file = yaml_data.parse_string(file_contents).asList()
        loc_file_dict = convert_to_dictionary(parsed_loc_file)
        loc_file_dict['file'] = file_path
        dict_list.append(loc_file_dict)
        
    except Exception as e:
        print(file_path)
        print(e)
        exit()

json.dump(dict_list, open('localisation-by-file.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)