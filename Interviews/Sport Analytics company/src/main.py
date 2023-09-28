from argparse import ArgumentParser
import logging
from utils import file_methods, db_methods
import data_process
import os
logging.basicConfig(level=logging.INFO)

# TODO: Add integrity checks.
# TODO: Add tests.

parser = ArgumentParser()
parser.add_argument("--db_location", dest="db_location", help="Location of the DB", default="files/db/cricsheet.db")
parser.add_argument("--data_url", dest="data_url", help="URL in which the data (.zip) can be found", default="https://cricsheet.org/downloads/all_json.zip")
parser.add_argument("--zip_data_path", dest="zip_file_path", help="Path in which to store the zip file", default="files/zip/all_json.zip")
parser.add_argument("--json_data_path", dest="json_data_path", help="Path in which to store the JSON files", default="files/json/")

if __name__ == "__main__":
    args = parser.parse_args()

    json_files = file_methods.download_and_get_json_files(args.data_url, args.zip_file_path, args.json_data_path)
    sqlite = db_methods.get_sqlite_connection(args.db_location)  # DB is already created!
    i = 1
    for json_file in json_files:
        logging.info(f"Processing file {i}/{len(json_files)}")
        data = file_methods.parse_json_file(os.path.join(args.json_data_path, json_file))
        try:
            data_process.insert_match(sqlite, data)
        except Exception as e:
            logging.error(f"Error processing file {json_file}. Error: {e}")
        i += 1
    db_methods.close_sqlite_connection()
    logging.info("Process finished successfully!")

