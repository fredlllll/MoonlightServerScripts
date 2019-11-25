import requests
from ChooseMethod import Method, ChooseMethod


def _parse_mod_ids_file(file):
    mod_ids = []

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        if len(line) > 0 and line[0] != '#':
            mod_ids.append(int(line))

    return mod_ids


def run_parse_mod_ids_file():
    mod_ids_file = input("path to mod id file:")
    return _parse_mod_ids_file(mod_ids_file)


def _get_collection_mod_ids(_collection_id):
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
            print("found file id: " + mod_id)
            ids.append(mod_id)
        return ids
    return []


def run_get_collection_mod_ids():
    collection_id = int(input("collection id:"))
    return _get_collection_mod_ids(collection_id)


def get_mod_ids():
    methods = [
        Method("Use Mod Id File", run_parse_mod_ids_file),
        Method("Use Steam Collection Id", run_get_collection_mod_ids)
    ]

    choose_methods = ChooseMethod(methods)

    return choose_methods.choose()
