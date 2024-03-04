import pytest
import sys
import os

# Append the directory containing coding_assesment.py to sys.path (To be able to run the tests from the command line)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coding_assesment import extract_user_agent_info, process_user_agent

# Sample user agent strings for tests
MOBILE_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.3 Mobile/15E148 Safari/604.1'
TABLET_UA = 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
PC_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537'
UNKNOWN_UA = 'Some Unknown User Agent'

def test_extract_user_agent_info():
    # Test mobile device type
    device, browser, version = extract_user_agent_info(MOBILE_UA)
    assert device == 'Mobile'
    assert browser == 'Mobile Safari'
    assert version == '13.3'

    # Test tablet device type
    device, browser, version = extract_user_agent_info(TABLET_UA)
    assert device == 'Tablet'
    # Add browser and version assertions as needed

    # Test computer device type
    device, browser, version = extract_user_agent_info(PC_UA)
    assert device == 'Computer'
    # Add browser and version assertions as needed

    # Test unknown device type
    device, browser, version = extract_user_agent_info(UNKNOWN_UA)
    assert device == 'Other'
    # Add browser and version assertions as needed

def test_process_user_agent():
    # Test with a valid user agent
    record = {'USER_AGENT': MOBILE_UA}
    processed = process_user_agent(record)
    assert processed['DEVICE'] == 'Mobile'
    assert processed['BROWSER'] == 'Mobile Safari'
    assert processed['VERSION'] == '13.3'

    # Test with missing user agent
    record = {'USER_AGENT': None}
    processed = process_user_agent(record)
    assert processed['DEVICE'] is None
    assert processed['BROWSER'] is None
    assert processed['VERSION'] is None

    # Test with malformed user agent
    record = {'USER_AGENT': 12345}
    with pytest.raises(Exception):
        process_user_agent(record)

