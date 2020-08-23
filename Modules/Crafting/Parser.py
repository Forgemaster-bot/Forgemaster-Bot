import yaml
import os

config_env_var = "CRAFTING_CONFIG_PATH"
default_path = os.path.join('Credentials')


def get_path():
    """
    Returns the path to patreon config file, prioritizing config_env_var env var.
    :return: patreon config file path
    """
    environment_path = os.getenv(config_env_var)
    return default_path if environment_path is None else environment_path


def parse_file(file_label):
    """
    Returns container storing data from <file_label>.yml yaml file
    :param file_label: name portion of filename
    :return: container storing data from yaml file
    """
    filename = '{}.yml'.format(file_label)
    path = os.path.join(get_path(), filename)
    with open(path, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


