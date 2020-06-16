LOG_FILE_LOCATION = './default.log'
WEB_DOMAIN = 'http://34.74.86.112'
APPLICATION_NAME = 'Moonlight Dashboard'

SESSION_COOKIE_NAME = "moondash_session_id"

MONGO_DB_DB_NAME = "moondash"
MONGO_DB_HOST = "127.0.0.1"
MONGO_DB_PORT = 27017

from TornadoBaseFramework.TornadoApplication import TORNADO_APPLICATION, HTTP_ENDPOINT

TORNADO_APPLICATIONS = {
    "tornado": TORNADO_APPLICATION("AWO2Q97KZPCQB8IBX1GO3XH3HB1PYPSCUOLVLSZP", [
        HTTP_ENDPOINT(True, 80)
    ])
}

PERMISSION_ADMIN = 'admin'
PERMISSION_EXPERIMENTAL = 'experimental'
PERMISSIONS = [
    PERMISSION_ADMIN,
    PERMISSION_EXPERIMENTAL
]

ARMA3APPID = 107410

import os

STEAMFOLDER = '/home/moonlight/.steam'
ARMA3SERVERDIR = os.path.join(STEAMFOLDER, 'SteamApps/common/Arma 3 Server')
ARMA3MODSDIR = os.path.join(ARMA3SERVERDIR, 'mods')
ARMA3SERVERSERVICENAME = 'arma3server'

ARMA3SERVERADDITONALCOMMANDLINE = "-cfg=basic.cfg -config=server.cfg -name=server -loadMissionToMemory"
ARMA3SERVERRUNSCRIPT = '/home/moonlight/runarma3server.sh'

BASE_HANDLER_CLASS = "Handlers.MoonlightBaseHandler.MoonlightBaseHandler"