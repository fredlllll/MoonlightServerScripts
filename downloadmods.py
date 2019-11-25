#!/usr/bin/python3.8
import subprocess
import os
import requests
import stat
import getpass

ARMA3APPID = 107410

STEAMFOLDER = '/home/moonlight/.steam'
ARMA3SERVERDIR = os.path.join(STEAMFOLDER, 'SteamApps/common/Arma 3 Server')


def parse_mod_ids_file(file):
    mod_ids = []

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        if len(line) > 0 and line[0] != '#':
            mod_ids.append(int(line))

    return mod_ids


def get_collection_mod_ids(_collection_id):
    # gives you a list of all mod ids in a workshop collection
    # info taken from https://steamapi.xpaw.me/#ISteamRemoteStorage/GetCollectionDetails
    form_data = {
        'collectioncount': 1,
        'publishedfileids[0]': _collection_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/?", data=form_data)

    if resp.status_code == 200:
        items = resp.json()['response']['collectiondetails'][0]['children']
        ids = []
        for item in items:
            mod_id = item['publishedfileid']
            print("found file id: " + mod_id + "\n")
            ids.append(mod_id)
        return ids
    return []


def download_mods(mod_ids):
    commands = []
    for mod_id in mod_ids:
        commands.append('+workshop_download_item')
        commands.append(str(ARMA3APPID))
        commands.append(str(mod_id))
    run_steam_cmd(commands)

    # wird nach "/home/moonlight/.steam/SteamApps/workshop/content/107410/450814997" gedownloaded


def run_steam_cmd(parameters):
    steam_user = input('Steam user pls:')
    steam_password = getpass.getpass('Steam password pls:')

    subprocess.check_call(["/usr/games/steamcmd", '+login', steam_user, steam_password] + parameters + ['+quit'])
    print("\n")


def escape_mod_name(mod_name):
    # best guess are that these are escaped: / < > : " \ | ? * with a dash cause they dont work on windows
    to_escape = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']

    for c in to_escape:
        mod_name = mod_name.replace(c, '-')
    return mod_name


def process_mod_links(mod_ids):
    # make links to the mods folders
    mods_dir = os.path.join(ARMA3SERVERDIR, 'mods')

    mod_paths = []
    for mod_id in mod_ids:
        mod_name = escape_mod_name(get_mod_name(mod_id))
        link_path = os.path.join(mods_dir, '@' + mod_name)
        if os.path.exists(link_path):
            continue  # dont do anything if the link is already in place
        mod_path = os.path.join(STEAMFOLDER, 'SteamApps/workshop/content', str(ARMA3APPID), str(mod_id))
        os.symlink(mod_path, link_path, target_is_directory=True)
        mod_paths.append(link_path)
    return mod_paths


def get_mod_name(_id):
    form_data = {
        'itemcount': 1,
        'publishedfileids[0]': _id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?", data=form_data)
    if resp.status_code != 200:  # just return id if the call failed
        return str(_id)
    return resp.json()['response']['publishedfiledetails'][0]['title']


def create_server_run_script_content(mod_paths):
    rel_paths = []
    for path in mod_paths:
        rel = os.path.relpath(path, ARMA3SERVERDIR)  # should return something like mods/@lalala
        rel_paths.append(rel)

    content = "#!/bin/bash\n"
    content += 'cd "' + ARMA3SERVERDIR + '"\n'
    content += './arma3server -config=server.cfg -name=server -mod="\\\n'

    for mod_path in rel_paths:
        content += mod_path + ';\\\n'

    content += '"'

    return content


def process_mod_ids_list(mod_ids):
    download_mods(mod_ids)
    mod_paths = process_mod_links(mod_ids)
    mod_param = create_server_run_script_content(mod_paths)
    with open("runarma3server.sh", "w") as f:
        f.write(mod_param)
    os.chmod("runarma3server.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)


def run__use_mod_ids_file():
    mod_ids_file = input("path to mod id file:")
    mod_ids = parse_mod_ids_file(mod_ids_file)
    process_mod_ids_list(mod_ids)


def run__use_steam_collection_id():
    collection_id = int(input("collection id:"))
    mod_ids = get_collection_mod_ids(collection_id)
    process_mod_ids_list(mod_ids)


options = [
    {
        "name": "Use Mod Id File",
        "method": run__use_mod_ids_file
    },
    {
        "name": "Use Steam Collection Id",
        "method": run__use_steam_collection_id
    }
]

print("valid options are:\n")
for i in range(len(options)):
    print(str(i) + ') ' + options[i]['name'] + "\n")

chosen_option = int(input("Choose option:"))
options[chosen_option]['method']()
