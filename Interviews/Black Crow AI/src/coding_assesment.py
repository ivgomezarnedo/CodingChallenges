import gzip
import json
from user_agents import parse
import logging
logging.basicConfig(level=logging.INFO)

input_file_path = "files/sample_orders.json.gz"
output_file_path = "files/sample_orders_transformed.json.gz"


def extract_user_agent_info(user_agent_str):
    """
    Extracts device type, browser type and browser version from user agent string
    :param user_agent_str:
    :return: device_type, browser_type, browser_version
    """
    user_agent = parse(user_agent_str)
    # Extracting device type
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'Computer'
    else:
        device_type = 'Other'

    browser_type = user_agent.browser.family
    browser_version = user_agent.browser.version_string
    return device_type, browser_type, browser_version

def process_user_agent(record):
    """
    Processes user agent string and adds device type, browser type and browser version to the record. If user agent
    string is not present, device type, browser type and browser version are set to None.
    :param record:
    :return: processed_record
    """
    if record['USER_AGENT']:
        record['DEVICE'], record['BROWSER'], record['VERSION'] = extract_user_agent_info(record['USER_AGENT'])
    else:
        record['DEVICE'] = None
        record['BROWSER'] = None
        record['VERSION'] = None
    return record


if __name__ == "__main__":
    logging.info(f"Starting...")
    records = []
    with gzip.open(input_file_path, 'rt', encoding='utf-8') as infile:
        for line in infile:
            record = json.loads(line)
            new_record = process_user_agent(record)
            records.append(new_record)

    with gzip.open(output_file_path, 'wt', encoding='utf-8') as outfile:
        for record in records:
            outfile.write(json.dumps(record) + '\n')  # Adding newline to maintain JSON Lines format
    logging.info(f"Successfully completed!")

