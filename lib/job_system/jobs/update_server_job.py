from lib.job_system.job import Job
from lib.apis.steam import update_server


class UpdateServerJob(Job):
    def __init__(self, user: str, password: str, auth_code: str):
        super().__init__('Update Server', 'Update Server')
        self.user: str = user
        self.password: str = password
        self.auth_code: str = auth_code

    def _run(self):
        update_server(self.user, self.password, self.auth_code)
