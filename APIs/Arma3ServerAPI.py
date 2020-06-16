from TornadoBaseFramework.Settings import Settings
import platform

print(platform.system())
if platform.system().lower() == 'windows':
    from TornadoBaseFramework.WindowsServiceController import WindowsServiceController

    Arma3ServerController = WindowsServiceController(Settings.ARMA3SERVERSERVICENAME)
else:
    from TornadoBaseFramework.SystemdUnitController import SystemdUnitController

    Arma3ServerController = SystemdUnitController(Settings.ARMA3SERVERSERVICENAME)
