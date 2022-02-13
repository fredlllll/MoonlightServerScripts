import subprocess
from lib.service_controller import ServiceController

class SystemdUnitController(ServiceController):
    def __init__(self, unit_name):
        self.unit_name = unit_name

    def enable(self):
        subprocess.check_call(['sudo', 'systemctl', 'enable', self.unit_name])

    def disable(self):
        subprocess.check_call(['sudo', 'systemctl', 'disable', self.unit_name])

    def stop(self):
        subprocess.check_call(['sudo', 'systemctl', 'stop', self.unit_name])

    def start(self):
        subprocess.check_call(['sudo', 'systemctl', 'start', self.unit_name])

    def restart(self):
        subprocess.check_call(['sudo', 'systemctl', 'restart', self.unit_name])

    def get_info(self):
        results = subprocess.check_output(['systemctl', 'show', self.unit_name, '--no-page'], universal_newlines=True).split('\n')
        results_dict = {}
        for entry in results:
            kv = entry.split(b"=", 1)
            if len(kv) == 2:
                results_dict[kv[0].decode()] = kv[1].decode()
        return results_dict

    def get_state(self):
        info = self.get_info()

        active_state = info.get('ActiveState', 'unknown')
        sub_state = info.get('SubState', 'unknown')
        return active_state + ', ' + sub_state

    def get_log(self, lines):
        return subprocess.check_output(['sudo', 'journalctl', '-u', self.unit_name, '-n' + str(int(lines)), '--no-pager'], universal_newlines=True)