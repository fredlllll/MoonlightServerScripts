from sanic import Sanic, Blueprint
from lib.middleware.user_session import user_session
from lib.middleware.logged_in_out import logged_in, logged_out
from lib.settings import Settings
from lib.db.migrations.migrations import run_migrations

# pages
from lib.page.index import index, index_post
from lib.page.jobs import jobs, jobs_post
from lib.page.login import login, login_post, logout
from lib.page.mod_downloader import mod_downloader, mod_downloader_post
from lib.page.mod_linker import mod_linker, mod_linker_post
from lib.page.new_server import new_server, new_server_post
from lib.page.register import register, register_post
from lib.page.server import server, server_post
from lib.page.servers import servers, servers_post
from lib.page.startup_script_maker import startup_script_maker, startup_script_maker_post


# apis


async def main_process_start(app, loop):
    print('running migrations')
    await run_migrations()


class SanicApp:
    def __init__(self):
        self.app = Sanic('sanic')

    def _register_listeners(self):
        self.app.register_listener(main_process_start, 'main_process_start')

    def _create_blueprints(self):
        self.bp_api_logged_in = Blueprint('api_logged_in', url_prefix='/api/v1/')  # api only accessible when logged in
        self.bp_logged_in = Blueprint('page_logged_in')  # pages only accessible when logged in
        self.bp_logged_out = Blueprint('page_logged_out')  # pages only accessible when logged out
        self.bp = Blueprint('page')  # pages accessible all the time
        self.bp_static = Blueprint('static')

    def _add_blueprints(self):
        self.app.blueprint(self.bp_api_logged_in)
        self.app.blueprint(self.bp_logged_in)
        self.app.blueprint(self.bp_logged_out)
        self.app.blueprint(self.bp)
        self.app.blueprint(self.bp_static)

    def _setup_middleware(self):
        self.bp_api_logged_in.middleware(user_session, 'request')
        self.bp_api_logged_in.middleware(logged_in, 'request')

        self.bp_logged_in.middleware(user_session, 'request')
        self.bp_logged_in.middleware(logged_in, 'request')

        self.bp_logged_out.middleware(user_session, 'request')
        self.bp_logged_out.middleware(logged_out, 'request')

        self.bp.middleware(user_session, 'request')

    def _setup_pages(self):
        self.bp_logged_in.add_route(index, '/', methods=('GET',))
        self.bp_logged_in.add_route(index_post, '/', methods=('POST',))

        self.bp_logged_in.add_route(jobs, '/jobs', methods=('GET',))
        self.bp_logged_in.add_route(jobs_post, '/jobs', methods=('POST',))

        self.bp_logged_out.add_route(login, '/login', methods=('GET',))
        self.bp_logged_out.add_route(login_post, '/login', methods=('POST',))
        self.bp_logged_in.add_route(logout, '/logout', methods=('GET',))

        self.bp_logged_in.add_route(mod_downloader, '/mod_downloader', methods=('GET',))
        self.bp_logged_in.add_route(mod_downloader_post, '/mod_downloader', methods=('POST',))

        self.bp_logged_in.add_route(mod_linker, '/mod_linker', methods=('GET',))
        self.bp_logged_in.add_route(mod_linker_post, '/mod_linker', methods=('POST',))

        self.bp_logged_in.add_route(new_server, '/new_server', methods=('GET',))
        self.bp_logged_in.add_route(new_server_post, '/new_server', methods=('POST',))

        self.bp_logged_out.add_route(register, '/register', methods=('GET',))
        self.bp_logged_out.add_route(register_post, '/register', methods=('POST',))

        self.bp_logged_in.add_route(server, '/servers/<server_id:str>', methods=('GET',))
        self.bp_logged_in.add_route(server_post, '/servers/<server_id:str>', methods=('POST',))

        self.bp_logged_in.add_route(servers, '/servers', methods=('GET',))
        self.bp_logged_in.add_route(servers_post, '/servers', methods=('POST',))

        self.bp_logged_in.add_route(startup_script_maker, '/startup_script_maker', methods=('GET',))
        self.bp_logged_in.add_route(startup_script_maker_post, '/startup_script_maker', methods=('POST',))

    def _setup_apis(self):
        pass

    def _setup_statics(self):
        self.bp_static.static('/static', './static', stream_large_files=True)

    def setup(self):
        self._register_listeners()
        self._create_blueprints()
        self._setup_middleware()
        self._setup_pages()
        self._setup_apis()
        self._setup_statics()
        self._add_blueprints()

    def run(self):
        self.app.run(host=Settings.sanic_host, port=Settings.sanic_port, access_log=Settings.access_log, workers=Settings.sanic_workers, auto_reload=False)
