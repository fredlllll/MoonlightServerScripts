from lib.job_system.job import Job
from lib.apis.steam import update_server


class UpdateServerJob(Job):
    def __init__(self, beta: str = None):
        super().__init__('Update Server', 'Update Server')

        self.beta = beta

    def _run(self):
        update_server(self.beta)
