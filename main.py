#!/usr/bin/python3.8
import subprocess
import os
import requests
import shutil

ARMA3APPID = 107410

STEAMFOLDER = '/home/moonlight/.steam'
ARMA3SERVERDIR = os.path.join(STEAMFOLDER,'SteamApps/common/Arma 3 Server')

def parseModIdsFile(file):
    _mod_ids = []

    with open(file) as f:
        lines = f.readlines()
        
    for line in lines:
        if len(line)>0 and line[0] != '#':
            _mod_ids.append(int(line))
    
    return _mod_ids;

def getCollectionModIds(_collection_id):
    #taken from https://steamapi.xpaw.me/#ISteamRemoteStorage/GetCollectionDetails
    form_data = {
        'collectioncount':1,
        'publishedfileids[0]':_collection_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/?",data=form_data)
    
    items = resp.json()['response']['collectiondetails'][0]['children']
    ids = []
    for item in items:
        id = item['publishedfileid']
        print("found file id: "+id+"\n")
        ids.append(id)   
    return ids
            
def downloadModsById(_mod_ids):
    commands = []
    for id in _mod_ids:
        commands.append('+workshop_download_item')
        commands.append(str(ARMA3APPID))
        commands.append(str(id))
    runSteamCMD(commands)
    
    #wird nach "/home/moonlight/.steam/SteamApps/workshop/content/107410/450814997" gedownloaded
    
def runSteamCMD(parameters = []):
    #TODO: ask for steam guard code
    steam_user = input('Steam user pls:')
    steam_password = input('Steam password pls:')

    subprocess.check_call(["/usr/games/steamcmd", '+login', steam_user, steam_password] + parameters + ['+quit'])
    print("\n")
    
def escapeModName(mod_name):
    #best guess are that these are escaped: / < > : " \ | ? *
    to_escape = ['/','<','>',':','"','\\','|','?','*']

    for c in to_escape:
        mod_name = mod_name.replace(c,'-')
    return mod_name
    
def copyMods(_mod_ids):
    #copy mods to the arma 3 server mods directory
    to_paths = []
    for id in _mod_ids:
        print("copying mod "+str(id)+"\n")
        from_path = os.path.join(STEAMFOLDER,'SteamApps/workshop/content',str(ARMA3APPID),str(id))
        mod_name = getModName(id)
        mod_name = escapeModName(mod_name)
        to_path = os.path.join(ARMA3SERVERDIR,'mods', '@'+mod_name)
        shutil.copytree(from_path,to_path, dirs_exist_ok=True)
        to_paths.append(to_path)
        
    return to_paths
        
        
def getModName(_id):
    form_data = {
        'itemcount':1,
        'publishedfileids[0]':_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?",data=form_data)
    if resp.status_code != 200: #just return id if the call failed
        return str(_id)
    return resp.json()['response']['publishedfiledetails'][0]['title']
    
def createModParameterContent(_mod_paths):
    rel_paths = []
    for path in _mod_paths:
        rel = os.path.relpath(path,ARMA3SERVERDIR)# should return something like mods/@lalala
        rel_paths.append(rel)
    return ";".join(rel_paths)
    
def downloadCopyMods(_mod_ids):
    downloadModsById(_mod_ids)
    mod_paths = copyMods(_mod_ids)
    mod_param = createModParameterContent(mod_paths)
    with open("mod_param.txt","w") as f:
        f.write(mod_param)
    
def run_useModIdFile():
    _mod_id_file = input("path to mod id file:")
    _mod_ids = parseModIdsFile(_mod_id_file)
    downloadCopyMods(_mod_ids)

def run_useSteamCollectionId():
    collection_id = int(input("collection id:"))
    _mod_ids = getCollectionModIds(collection_id)
    downloadCopyMods(_mod_ids)
    
options = [
    {
        "name":"Use Mod Id File",
        "method": run_useModIdFile
    },
    {
        "name":"Use Steam Collection Id",
        "method": run_useSteamCollectionId
    }
]

print("valid options are:\n")
for i in range(len(options)):
    print(str(i)+') '+options[i]['name']+"\n")
    
chosen_option = int(input("Choose option:"))
options[chosen_option]['method']()

    
