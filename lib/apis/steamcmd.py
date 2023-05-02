import subprocess
import logging
import os
from lib.settings import Settings
from typing import List, Optional
from lib.sync_tailers import ProcessTailer

logger = logging.getLogger(__name__)


class SteamCmd:
    user = None

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.tailer: Optional[ProcessTailer] = None

    @classmethod
    def _create_steam_cmd_call(cls, parameters: List[str], user: str = None, password: str = None, auth_code: str = None) -> List[str]:
        cmdline = ["/usr/games/steamcmd"]
        user = user or cls.user
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

    def _run_commandline(self, cmdline):
        try:
            env = os.environ.copy()
            env['HOME'] = os.path.expanduser(f'~{Settings.local_steam_user}')
            env['LOGNAME'] = Settings.local_steam_user
            env['PWD'] = os.getcwd()
            env['USER'] = Settings.local_steam_user
            self.process = subprocess.Popen(cmdline, bufsize=0, user=Settings.local_steam_user, group=Settings.local_steam_user, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.tailer = ProcessTailer(self.process, "steamcmd")
            self.tailer.start()
            # subprocess.check_call(cmdline, user=Settings.local_steam_user, group=Settings.local_steam_user, env=env, stdout=self.log_file, stderr=self.log_file)
        except subprocess.CalledProcessError as e:
            logger.warning("received non zero return code from steamcmd command: " + str(e.returncode))

    def login(self, user: str, password: str, auth_code: str = None):
        cmdline = self._create_steam_cmd_call([], user, password, auth_code)
        logger.info("logging in steamcmd")
        SteamCmd.user = user
        self._run_commandline(cmdline)

    def run(self, parameters: List[str]):
        cmdline = self._create_steam_cmd_call(parameters)
        logger.info("calling steamcmd: " + ' '.join(cmdline))
        self._run_commandline(cmdline)

    def wait(self):
        self.process.wait()
        self.tailer.join()
