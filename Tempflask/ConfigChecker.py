from configparser import ConfigParser


def check_config(secs: dict | ConfigParser, match_keys_list: list) -> tuple[bool, list]:
    missing_keys = [i for i in match_keys_list if i not in secs.keys()]
    if missing_keys:
        return False, missing_keys
    else:
        return True, missing_keys