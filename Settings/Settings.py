LOG_FILE_LOCATION = './default.log'
WEB_DOMAIN = 'http://34.74.86.112'
APPLICATION_NAME = 'Moonlight Dashboard'

SESSION_COOKIE_NAME = "moondash_session_id"


class MONGO_DB:
    host = "127.0.0.1"
    port = 27017
    db_name = "moondash"


from Framework.TornadoApplication import TORNADO_APPLICATION, HTTPS_ENDPOINT, HTTP_ENDPOINT

TORNADO_APPLICATIONS = {
    "tornado": TORNADO_APPLICATION("AWO2Q97KZPCQB8IBX1GO3XH3HB1PYPSCUOLVLSZP", [
        HTTPS_ENDPOINT(False, 443, "fullchain.pem", "privkey.pem"),
        HTTP_ENDPOINT(True, 80)
    ])
}

DEFAULT_USER_VALUES = {

}

PERMISSION_ADMIN = 'admin'
PERMISSION_EXPERIMENTAL = 'experimental'
PERMISSIONS = [
    PERMISSION_ADMIN,
    PERMISSION_EXPERIMENTAL
]

WEBHOOKS = {
}

ARMA3APPID = 107410

import os

STEAMFOLDER = '/home/moonlight/.steam'
ARMA3SERVERDIR = os.path.join(STEAMFOLDER, 'SteamApps/common/Arma 3 Server')
ARMA3MODSDIR = os.path.join(ARMA3SERVERDIR, 'mods')
ARMA3SERVERSERVICENAME = 'arma3server'

ARMA3SERVERRUNSCRIPT = '/home/moonlight/runarma3server.sh'

try:
    import Settings.LocalSettings
except Exception as e:
    print(str(e))
    pass
