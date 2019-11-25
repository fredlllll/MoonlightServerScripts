from STATICS import *
import getpass
import subprocess


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
