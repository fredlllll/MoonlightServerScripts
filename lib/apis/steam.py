import requests
from lib.constants import ARMA3APPID, ARMA3SERVERAPPID
import os
import logging
import shutil
from diskcache import Cache
from lib.acf import AcfFile
from typing import List, Tuple
from lib.settings import Settings
from lib.apis.steamcmd import SteamCmd

logger = logging.getLogger(__name__)

mod_name_cache = Cache(directory='caches/mod_names')


def get_steam_folder_path():
    return os.path.join(os.path.expanduser(f'~{Settings.local_steam_user}'), Settings.steam_dir_name)


def get_workshop_mods_folder():
    return os.path.join(get_steam_folder_path(), 'steamapps/workshop/content/', str(ARMA3APPID))


def get_arma_3_server_folder():
    return os.path.join(get_steam_folder_path(), 'steamapps/common/Arma 3 Server')


def get_arma_workshop_acf_path():
    return os.path.join(get_steam_folder_path(), f'steamapps/workshop/appworkshop_{ARMA3APPID}.acf')


def get_mod_name(mod_id: str, dont_use_cache: bool = False) -> str:
    name: str = ''
    if not dont_use_cache:
        name = mod_name_cache.get(mod_id, None)
        if name is not None:
            return name
    form_data = {
        'itemcount': 1,
        'publishedfileids[0]': mod_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?", data=form_data)
    if resp.status_code != 200:  # just return id if the call failed
        name = str(mod_id)
    else:
        try:
            name = resp.json()['response']['publishedfiledetails'][0]['title']
            mod_name_cache.set(mod_id, name)
        except KeyError:
            name = str(mod_id)

    return name


def escape_mod_name(mod_name: str) -> str:
    # best guess is that these are escaped: / < > : " \ | ? * with a dash cause they dont work on windows
    to_escape = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']

    for c in to_escape:
        mod_name = mod_name.replace(c, '-')
    return mod_name


def get_collection_mod_ids(collection_id: str) -> List[str]:
    # gives you a list of all mod ids in a workshop collection
    # info taken from https://steamapi.xpaw.me/#ISteamRemoteStorage/GetCollectionDetails
    form_data = {
        'collectioncount': 1,
        'publishedfileids[0]': collection_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/?", data=form_data)

    if resp.status_code == 200:
        first_collection = resp.json()['response']['collectiondetails'][0]
        items = first_collection.get('children', [])
        ids = []
        for item in items:
            mod_id = item['publishedfileid']
            ids.append(str(mod_id))
        return ids
    else:
        logger.warning(resp.content)
    return []


def download_mods(mod_ids: List[str]):
    commands: List[str] = []
    for mod_id in mod_ids:
        commands.append('+workshop_download_item')
        commands.append(str(ARMA3APPID))
        commands.append(str(mod_id))
    steamcmd = SteamCmd()
    steamcmd.run(commands)
    steamcmd.wait()


def get_downloaded_mods() -> List[str]:
    mods = []

    workshop_mods_folder = get_workshop_mods_folder()
    if os.path.exists(workshop_mods_folder):
        for entry in os.listdir(workshop_mods_folder):
            if os.path.isdir(os.path.join(workshop_mods_folder, entry)):
                mods.append(entry)

    return mods


def delete_downloaded_mods(mod_ids: List[str]):
    # delete mods from the steams acf file
    arma_acf_file = get_arma_workshop_acf_path()
    acf = AcfFile(arma_acf_file)
    items_installed = acf.root.nodes["WorkshopItemsInstalled"]
    item_details = acf.root.nodes["WorkshopItemDetails"]
    keys = list(items_installed.nodes.keys())
    for k in keys:
        if k in mod_ids:
            del items_installed.nodes[k]
            del item_details.nodes[k]
    acf.save()

    workshop_mods_folder = get_workshop_mods_folder()
    for mod_id in mod_ids:
        mod_folder = os.path.join(workshop_mods_folder, mod_id)
        if os.path.exists(mod_folder):
            shutil.rmtree(mod_folder, ignore_errors=True)


def app_update(appid: str, *, validate=True, beta: str = None):
    beta_str = (" -beta " + beta + " ''") if beta else ""  # no idea if it works without the '' in there
    commands: List[str] = [
        f'+app_update {appid}{beta_str}{" validate" if validate else ""}'
    ]
    steamcmd = SteamCmd()
    steamcmd.run(commands)
    steamcmd.wait()


def update_server(beta: str = None):
    app_update(ARMA3SERVERAPPID, beta=beta)
