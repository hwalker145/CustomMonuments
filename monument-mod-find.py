# this works

import os
import json
import sqlite3
import pathlib

launcher_db_path = "C:/Users/walkerh4/Documents/Paradox Interactive/Europa Universalis IV/launcher-v2.sqlite"
euiv_path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/236850"
mods_dir = os.listdir(euiv_path)
paths = []
manifest_path = "monument-mod-manifest.json"

# grabbing the playset names from the .sqlite
db_connect = sqlite3.connect(launcher_db_path)
cursor = db_connect.cursor()

query = "SELECT name FROM playsets"

cursor.execute(query)
results = cursor.fetchall()
##

# requesting the playset desired to mod
print("SELECT THE PLAYSET YOU WANT TO MOD\n")
for i, playset_name in enumerate(results):
    print(f"{i + 1}. {max(playset_name)}")

playset_name_selected = max(results[int(input()) - 1])
##

# grabbing the list of mod directories that are in that playset
query = "SELECT mods.steamId FROM mods\n" + \
        "JOIN playsets_mods ON mods.id = playsets_mods.modId\n" + \
        "JOIN playsets ON playsets_mods.playsetId = playsets.id\n" + \
        f"WHERE playsets.name = \'{playset_name_selected}\'"

cursor.execute(query)
results = cursor.fetchall()
playset_mods = [max(num) for num in results]
##

# taking only the mods from the playset
mods_dir = list(set(playset_mods).intersection(mods_dir))
##

# finding the monument-based mod directories for the selected playset
for euiv_dir_object in mods_dir:
    # if it is not a directory, skip
    if not os.path.isdir(os.path.join(euiv_path, euiv_dir_object)):
        continue
    # if it does not have a great projects directory, skip
    if not os.path.exists(os.path.join(euiv_path, euiv_dir_object, "common", "great_projects")):
        continue
    mod_dir = euiv_dir_object
    
    mod_dir_gp = os.path.join(euiv_path, mod_dir, "common", "great_projects")
    for gp_dir_object in os.listdir(mod_dir_gp):
        # print(gp_dir_object)
        if "monument" in gp_dir_object \
        or "GME" in gp_dir_object:
            paths.append(str(pathlib.WindowsPath(os.path.join(euiv_path, mod_dir))))
            break

# print(paths)

mod_manifest_data = json.load(open(manifest_path, 'r'))

if 'mods' in mod_manifest_data:
    mod_manifest_data['mods'] = paths
    # print(manifest_data)

json.dump(mod_manifest_data, open(manifest_path, 'w'), indent=4)