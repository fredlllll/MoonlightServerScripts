from lib.db.migrations.migrations_list import migrations
from lib.db.models.migration import Migration
import logging

logger = logging.getLogger(__name__)


async def run_migrations():
    done_migs = Migration.all()
    done_migs = [m.timestamp for m in done_migs]

    for m in migrations:
        if m.timestamp not in done_migs:
            await m.run(None)
            mig = Migration()
            mig.timestamp = m.timestamp
            mig.save()
