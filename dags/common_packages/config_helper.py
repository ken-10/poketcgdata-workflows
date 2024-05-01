import os.path

import yaml

from common_packages import secrets_helper

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))


def get_config(key: str, config_file_path: str = CONFIG_PATH) -> dict:
    environment = os.getenv(key="env", default="local")
    config_file_path = os.path.join(config_file_path, f"{environment}.yaml")
    with open(config_file_path, mode="r", encoding="UTF-8") as stream:
        config = yaml.safe_load(stream)[key]
    print(type(config))

    for config_key, config_val in config.items():
        if config_val.startswith("get_secret_"):
            config[config_key] = secrets_helper.get_variable(config_val)

    return config
