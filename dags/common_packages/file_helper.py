import logging
import os.path
import shutil


def create_folder(directory: str, new_folder_name: str) -> str:
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory {directory} does not exist")

    if not os.path.isdir(directory):
        raise OSError(f"Path {directory} is not a directory")

    new_folder_path = os.path.join(directory, new_folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        logging.info(f"Successfully created {new_folder_path}")
    else:
        logging.info(f"{new_folder_path} already exists")

    return new_folder_path

def delete_folder(folder_path: str):
    if not os.path.exists(folder_path):
        logging.info(f"{folder_path} does not exist")
        return

    if not os.path.isdir(folder_path):
        raise OSError(f"Path {folder_path} is not a directory")

    shutil.rmtree(folder_path)
    logging.info(f"Deleted {folder_path} successfully")

