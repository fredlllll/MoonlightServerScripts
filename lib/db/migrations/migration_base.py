class MigrationBase:
    def __init__(self, creation_timestamp):
        self.timestamp = creation_timestamp

    async def execute(self, session):
        pass

    async def run(self, session):
        print(f'running migration {self.timestamp}')
        await self.execute(session)
