from lib.settings import Settings
from lib.systemd_unit_controller import SystemdUnitController
from lib.mock_service_controller import MockServiceController
from lib.db.models.arma_3_modset import Arma3Modset
from lib.db.models.arma_3_modset_mod import Arma3ModsetMod
from lib.apis.steam import get_mod_name
import os
import subprocess
import platform

controllers = {}


def get_server_controller(server_id):
    cont = controllers.get(server_id, None)
    if cont is None:
        if "Windows" in platform.platform():
            cont = MockServiceController()
        else:
            cont = SystemdUnitController("arma3server_" + server_id + ".service")
        controllers[server_id] = cont
    return cont


async def create_startup_script(server):
    user = Settings.arma_3_server_user
    file_name = "/home/" + user + "/arma3server_" + server.id + "_startup.sh"

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.arma_3_server_dir + '"\n'
    content += f'./arma3server -cfg={server.id}_basic.cfg -config={server.id}_server.cfg ' + server.additional_commandline + ' -mod="\\\n'

    if server.modset_id:
        modset = Arma3Modset.find(server.modset_id)
        mods = Arma3ModsetMod.where({'modset_id': modset.id})

        for mod in mods:
            mod_name = get_mod_name(mod.mod_steam_id)
            abs_path = os.path.join(Settings.arma_3_mods_dir, mod_name)
            rel_path = os.path.relpath(abs_path, Settings.arma_3_server_dir)
            content += rel_path + ';\\\n'

    content += '"'

    with open(file_name, 'w') as f:
        f.write(content)


def create_service(server):
    '''creates a service file for the server, and calls daemon-reload'''
    file_name = "/etc/systemd/system/arma3server_" + server.id + ".service"
    user = Settings.arma_3_server_user

    content = "[Unit]\nDescription=Arma 3 Server\n\n[Service]\nUser="
    content += user
    content += "\nGroup=" + user
    content += "\nWorkingDirectory=/home/" + user
    content += "\nExecStart=/bin/bash /home/" + user + "/arma3server_" + server.id + "_startup.sh"
    content += "\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n"

    with open(file_name, 'w') as f:
        f.write(content)

    subprocess.check_call("sudo systemctl daemon-reload")
