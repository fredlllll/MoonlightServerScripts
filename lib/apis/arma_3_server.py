from lib.settings import Settings
from lib.systemd_unit_controller import SystemdUnitController
from lib.mock_service_controller import MockServiceController
import os
import getpass
import subprocess
import platform

if "Windows" in platform.platform():
    Arma3ServerController = MockServiceController()
else:
    Arma3ServerController = SystemdUnitController(Settings.arma_3_server_service_name)


def create_startup_script(server_id, additional_commandline, mod_ids):
    user = getpass.getuser()
    file_name = "/home/" + user + "/" + server_id + "_startup.sh"

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.arma_3_server_dir + '"\n'
    content += './arma3server ' + additional_commandline + ' -mod="\\\n'

    for mod in mod_ids:
        abs_path = os.path.join(Settings.arma_3_mods_dir, mod['name'])
        rel_path = os.path.relpath(abs_path, Settings.arma_3_server_dir)
        content += rel_path + ';\\\n'

    content += '"'

    with open(file_name, 'w') as f:
        f.write(content)


def create_service(server_id):
    '''creates a service file for the server, and calls daemon-reload'''
    file_name = "/etc/systemd/system/arma3server_" + server_id + ".service"
    user = getpass.getuser()

    content = "[Unit]\nDescription=Arma 3 Server\n\n[Service]\nUser="
    content += user
    content += "\nGroup=" + user
    content += "\nWorkingDirectory=/home/" + user
    content += "\nExecStart=/bin/bash /home/" + user + "/" + server_id + "_startup.sh"
    content += "\nRestart=always\n\n[Install]\nWantedBy=multi-user.target\n"

    with open(file_name, 'w') as f:
        f.write(content)

    subprocess.check_call("systemctl daemon-reload")
