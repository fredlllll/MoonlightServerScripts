import stat
from Util import escape_mod_name, get_mod_name
from STATICS import *


def create_server_run_script_content(mod_ids):
    mod_paths = []
    for mod_id in mod_ids:
        mod_name = escape_mod_name(get_mod_name(mod_id))
        link_path = os.path.join(ARMA3MODSDIR, '@' + mod_name)
        mod_paths.append(link_path)

    rel_paths = []
    for path in mod_paths:
        rel = os.path.relpath(path, ARMA3SERVERDIR)  # should return something like mods/@lalala
        rel_paths.append(rel)

    content = "#!/bin/bash\n"
    content += 'cd "' + ARMA3SERVERDIR + '"\n'
    content += './arma3server -config=server.cfg -name=server -mod="\\\n'

    for mod_path in rel_paths:
        content += mod_path + ';\\\n'

    content += '"'

    return content


def create_run_script(mod_ids):
    content = create_server_run_script_content(mod_ids)
    with open("runarma3server.sh", "w") as f:
        f.write(content)
    # make executable by owner
    os.chmod("runarma3server.sh", stat.S_IRWXU | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH)
