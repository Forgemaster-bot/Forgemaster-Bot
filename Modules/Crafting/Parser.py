import yaml
import os
import Connections


config_env_var = "CRAFTING_CONFIG_PATH"
default_path = os.path.join('yaml')


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
    filename = '{}.yaml'.format(file_label)
    path = os.path.join(get_path(), filename)
    with open(path, 'r') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


def get_files():
    return ['thaumstyn']


def parse_files():
    return {file_label: parse_file(file_label) for file_label in get_files()}


parsed_data = parse_files()


def refresh_file(file_label):
    global parsed_data
    parsed_data[file_label] = parse_file(file_label)


def get_parsed_data(file_label):
    global parsed_data
    return parsed_data[file_label]


