from Framework.Model import Model

WAITING = 'waiting'
EXECUTING = 'executing'
FINISHED = 'finished'
FAILED = 'failed'


class JobInfo(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'job_infos'

    def _get_fields(self):
        return [
            'name',
            'info',
            'status',
            'error',
            'start_timestamp',
            'end_timestamp',
            'progress'
        ]
