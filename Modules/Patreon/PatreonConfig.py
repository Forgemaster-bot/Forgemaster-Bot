import os
import json

config_env_var = "PATREON_CONFIG_PATH"
default_path = os.path.join('Credentials', 'PatreonConfig.json')


def get_path():
    """
    Returns the path to patreon config file, prioritizing PATREON_CONFIG_PATH env var.
    :return: patreon config file path
    """
    environment_path = os.getenv('PATREON_CONFIG_PATH')
    return default_path if environment_path is None else environment_path


def load_config(path):
    local_config = dict()
    with open(path, "r") as config_file:
        local_config = json.load(config_file)
    return local_config


def get_extra_character_role() -> str:
    config = load_config(get_path())
    return config["roles"]["extra-character"]


def is_enabled() -> bool:
    config = load_config(get_path())
    return config["enabled"]
