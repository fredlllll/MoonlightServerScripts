import requests
from subprocess import check_call


def is_string_truthy(s):
    return s.lower() in ['true', '1', 'y', 'yes']


def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


def escape_mod_name(mod_name):
    # best guess are that these are escaped: / < > : " \ | ? * with a dash cause they dont work on windows
    to_escape = ['/', '<', '>', ':', '"', '\\', '|', '?', '*']

    for c in to_escape:
        mod_name = mod_name.replace(c, '-')
    return mod_name


def get_mod_name(mod_id):
    form_data = {
        'itemcount': 1,
        'publishedfileids[0]': mod_id
    }
    resp = requests.post("https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/?", data=form_data)
    if resp.status_code != 200:  # just return id if the call failed
        return str(mod_id)
    return resp.json()['response']['publishedfiledetails'][0]['title']


def mount_dir(original_path, link_path):
    check_call(["mount", "--bind", original_path, link_path])
