from .ServiceController import ServiceController


class WindowsServiceController(ServiceController):
    '''
        this is a stub cause im just running this on linux for now. but i need it to test on windows
    '''

    def __init__(self, service_name):
        self.service_name = service_name

    def enable(self):
        pass

    def disable(self):
        pass

    def stop(self):
        pass

    def start(self):
        pass

    def restart(self):
        pass

    def get_info(self):
        return {"state": "dummy state"}

    def get_state(self):
        return "dummy state"

    def get_log(self, lines):
        return "dummy log"
