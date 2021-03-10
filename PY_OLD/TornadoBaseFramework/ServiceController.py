from abc import ABC, abstractmethod


class ServiceController(ABC):
    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_log(self, lines):
        pass
