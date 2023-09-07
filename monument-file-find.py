import os
import json
import pathlib

mod_manifest_path = "monument-mod-manifest.json"
mod_manifest_data = json.load(open(mod_manifest_path, 'r'))
files_paths_list = []

for mod_path in mod_manifest_data['mods']:
    gp_dir = os.path.join(mod_path, "common", "great_projects")
    
    for file in os.listdir(gp_dir):
        files_paths_list.append(str(pathlib.WindowsPath(os.path.join(mod_path, "common", "great_projects", file))))

file_manifest_path = "file-manifest.json"
file_manifest_data = json.load(open(file_manifest_path, 'r'))

if 'files' in file_manifest_data:
    file_manifest_data['files'] = files_paths_list

json.dump(file_manifest_data, open(file_manifest_path, 'w'), indent=4)