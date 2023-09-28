import json
import zipfile
import urllib.request
import os
import logging
logging.basicConfig(level=logging.INFO)


def _download_zip_file(url: str, zip_path: str):
    """
    Download a zip file from a given URL and store it in the given path
    :param url: URL from which to download the zip file
    :param zip_path: PATH in which to store the zip file
    :return:
    """
    zip_dir = os.path.dirname(zip_path)     # Ensure the parent directory of the zip file exists
    os.makedirs(zip_dir, exist_ok=True)
    try:
        logging.info(f"Downloading zip file from {url} and storing it in {zip_path}")
        urllib.request.urlretrieve(url, zip_path)
        logging.info(f"Zip file downloaded from {url} and stored in {zip_path}")
    except Exception as ex:
        logging.error(f"Failed to download data from {url}. Error: {ex}")
        raise ex


def parse_json_file(file_path: str) -> dict:
    """
    Parse a JSON file and return its contents
    :param file_path: PATH of the JSON file
    :return: JSON file contents
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def _extract_zip_and_get_files(zip_path: str, json_path: str) -> list:
    """
    Extract a zip file and return the list of JSON files extracted
    :param zip_path: PATH in which the zip file is located
    :param json_path: PATH in which to store the extracted JSON files
    :return: List of JSON files extracted
    """
    os.makedirs(json_path, exist_ok=True)  # Ensure the extraction directory exists
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(json_path)
    logging.info(f"Zip file extracted in {json_path}")

    # List all .json files in the extraction directory
    return [f for f in os.listdir(json_path) if f.endswith('.json')]


def download_and_get_json_files(url: str, zip_path: str, json_path: str) -> list:
    """
    Download a zip file from a given URL, extract it and return the list of JSON files extracted
    :param url: URL from which to download the zip file
    :param zip_path: PATH in which to store the zip file
    :param json_path: PATH in which to store the extracted JSON files
    :return: List of JSON files extracted
    """
    _download_zip_file(url, zip_path)
    return _extract_zip_and_get_files(zip_path, json_path)
