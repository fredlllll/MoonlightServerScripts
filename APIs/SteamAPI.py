import requests
from TornadoBaseFramework.Settings import Settings
import subprocess
import os
import logging
import shutil

logger = logging.getLogger(__name__)

MOD_NAME_CACHE = {}


def get_mod_name(mod_id, dont_use_cache=False):
    name = None
    if not dont_use_cache:
        name = MOD_NAME_CACHE.get(mod_id, None)
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
        name = resp.json()['response']['publishedfiledetails'][0]['title']

    MOD_NAME_CACHE[mod_id] = name

    return name


def escape_mod_name(mod_name):
    # best guess are that these are escaped: / < > : " \ | ? * with a dash cause they dont work on windows
    to_escape = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']

    for c in to_escape:
        mod_name = mod_name.replace(c, '-')
    return mod_name


def clear_mod_name_cache():
    global MOD_NAME_CACHE
    MOD_NAME_CACHE = {}


def get_collection_mod_ids(collection_id):
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
            print("found file id: " + mod_id)
            ids.append(mod_id)
        return ids
    return []


def download_mods(mod_ids, user, password, auth_code):
    commands = []
    for mod_id in mod_ids:
        commands.append('+workshop_download_item')
        commands.append(str(Settings.ARMA3APPID))
        commands.append(str(mod_id))
    run_steam_cmd(commands, user, password, auth_code)


def _create_steam_cmd_call(parameters, user=None, password=None, auth_code=None):
    cmdline = ["/usr/games/steamcmd"]
    if user is not None:
        cmdline.append('+login')
        cmdline.append(user)
        if password is not None:
            cmdline.append(password)
            if auth_code is not None:
                cmdline.append(auth_code)
    cmdline += parameters
    cmdline.append('+quit')
    return cmdline


def run_steam_cmd(parameters, user=None, password=None, auth_code=None):
    cmdline = _create_steam_cmd_call(parameters, user, password, auth_code)
    cmdline_censored = _create_steam_cmd_call(parameters, 'USER', 'PASSWORD', 'AUTH_CODE')  # prevent logging user credentials
    logger.info("calling steamcmd: " + ' '.join(cmdline_censored))
    try:
        subprocess.check_call(cmdline)
    except subprocess.CalledProcessError as e:
        logger.warning("received non zero return code from steamcmd command: " + str(e.returncode))


def get_downloaded_mods():
    mods = []

    workshop_mods_folder = os.path.join(Settings.STEAMFOLDER, 'SteamApps/workshop/content/', str(Settings.ARMA3APPID))
    if os.path.exists(workshop_mods_folder):
        for entry in os.listdir(workshop_mods_folder):
            if os.path.isdir(os.path.join(workshop_mods_folder, entry)):
                mods.append(entry)

    return mods


def delete_downloaded_mods(mod_ids):
    workshop_mods_folder = os.path.join(Settings.STEAMFOLDER, 'SteamApps/workshop/content/', str(Settings.ARMA3APPID))
    for mod_id in mod_ids:
        mod_folder = os.path.join(workshop_mods_folder, mod_id)
        if os.path.exists(mod_folder):
            shutil.rmtree(mod_folder, ignore_errors=True)
