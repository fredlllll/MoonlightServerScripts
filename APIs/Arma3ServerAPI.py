from TornadoBaseFramework.Settings import Settings
import platform
import os
import getpass
import subprocess

if platform.system().lower() == 'windows':
    from TornadoBaseFramework.WindowsServiceController import WindowsServiceController

    Arma3ServerController = WindowsServiceController(Settings.ARMA3SERVERSERVICENAME)
else:
    from TornadoBaseFramework.SystemdUnitController import SystemdUnitController

    Arma3ServerController = SystemdUnitController(Settings.ARMA3SERVERSERVICENAME)


def create_startup_script(server_id, additional_commandline, mod_ids):
    user = getpass.getuser()
    file_name = "/home/" + user + "/" + server_id + "_startup.sh"

    content = "#!/bin/bash\n"
    content += 'cd "' + Settings.ARMA3SERVERDIR + '"\n'
    content += './arma3server ' + additional_commandline + ' -mod="\\\n'

    for mod in mod_ids:
        abs_path = os.path.join(Settings.ARMA3MODSDIR, mod['name'])
        rel_path = os.path.relpath(abs_path, Settings.ARMA3SERVERDIR)
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
