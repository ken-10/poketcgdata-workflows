import logging

from airflow.models import Variable


def get_variable(key: str):
    if key.startswith("get_secret_"):
        variable_name = key.replace("get_secret_", "")
        logging.info(f"Attempting to get secret from variable {variable_name}")
        try:
            return Variable.get(variable_name)
        except KeyError as e:
            logging.info(f"Failed to get variable due to the following error: {str(e)} - Returning as {key}")
    return key
