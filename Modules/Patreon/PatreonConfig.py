import os
import json

config_env_var = "PATREON_CONFIG_PATH"
default_path = os.path.join('Credentials', 'PatreonConfig.json')


def get_path():
    """
    Returns the path to patreon config file, prioritizing config_env_var env var.
    :return: patreon config file path
    """
    environment_path = os.getenv(config_env_var)
    return default_path if environment_path is None else environment_path


def load_config(path) -> dict:
    """
    Returns dictionary containing data from patreon json file
    :param path: path to file
    :return: dictionary containing json data
    """
    with open(path, "r") as config_file:
        return json.load(config_file)


def get_extra_character_role() -> str:
    """
    Returns the name of the extra-character role
    :return: string name of role
    """
    config = load_config(get_path())
    return config["roles"]["extra-character"]


def is_enabled() -> bool:
    """
    Returns whether patreon feature are enabled or not.
    :return: boolean
    """
    config = load_config(get_path())
    return config["enabled"]
