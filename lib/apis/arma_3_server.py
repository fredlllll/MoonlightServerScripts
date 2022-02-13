from lib.settings import Settings
from lib.systemd_unit_controller import SystemdUnitController
from lib.mock_service_controller import MockServiceController
from lib.db.models.arma_3_server_mod import Arma3ServerMod
from lib.apis.steam import get_mod_name
import os
import subprocess
import platform

if "Windows" in platform.platform():
    Arma3ServerController = MockServiceController()
else:
    Arma3ServerController = SystemdUnitController(Settings.arma_3_server_service_name)

controllers = {}


def get_server_controller(server):
    cont = controllers.get(server.id, None)
    if cont is None:
        if "Windows" in platform.platform():
            cont = MockServiceController()
        else:
            cont = SystemdUnitController("arma3server_" + server.id + ".service")
        controllers[server.id] = cont
    return cont


async def create_startup_script(server):
    user = Settings.arma_3_server_user
    file_name = "/home/" + user + "/arma3server_" + server.id + "_startup.sh"

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.arma_3_server_dir + '"\n'
    content += f'./arma3server -cfg={server.id}_basic.cfg -config={server.id}_server.cfg ' + server.additional_commandline + ' -mod="\\\n'

    mods = await Arma3ServerMod.where({'server_id':server.id})

    for mod in mods:
        mod_name = get_mod_name(mod.mod_id)
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
