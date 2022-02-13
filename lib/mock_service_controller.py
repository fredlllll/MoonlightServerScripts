from lib.service_controller import ServiceController


class MockServiceController(ServiceController):
    def __init__(self):
        self.active_state = "disabled"
        self.sub_state = "stopped"

    def enable(self):
        self.active_state = "enabled"

    def disable(self):
        self.active_state = "disabled"

    def stop(self):
        self.sub_state = "stopped"

    def start(self):
        self.sub_state = "started"

    def restart(self):
        self.sub_state = "started"

    def get_info(self):
        results_dict = {"ActiveState": self.active_state, "SubState": self.sub_state}
        return results_dict

    def get_state(self):
        info = self.get_info()

        active_state = info.get('ActiveState', 'unknown')
        sub_state = info.get('SubState', 'unknown')
        return active_state + ', ' + sub_state

    def get_log(self, lines):
        return "this is a log or so"
