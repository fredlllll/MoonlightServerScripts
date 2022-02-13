import time
import os


def main():
    timestamp = int(time.time())
    file_name = f'migration_{timestamp}.py'
    with open(file_name, 'w') as f:
        f.write('from lib.db.migrations.migration_base import MigrationBase\n\n\n')
        f.write(f'class Migration{timestamp}(MigrationBase):\n')
        f.write(f'    def __init__(self):\n        super().__init__({timestamp})\n\n')
        f.write('    async def execute(self, session):\n        pass  # put your db changes here\n')

    files = os.listdir('.')
    all_migrations = []
    for fname in files:
        if fname.startswith('migration_'):
            all_migrations.append(fname.replace('migration_', '').replace('.py', ''))

    with open('migrations_list.py', 'w') as f:
        f.write('# this is a generated file, dont change it by hand\n')
        for mig in all_migrations:
            f.write(f'from lib.db.migrations.migration_{mig} import Migration{mig}\n')
        f.write('\nmigrations = [\n')
        for mig in all_migrations:
            f.write(f'    Migration{mig}(),\n')
        f.write(']\n')


if __name__ == '__main__':
    main()
