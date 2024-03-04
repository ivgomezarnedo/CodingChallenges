import json
import gzip
import datetime
import pytz
import pytest
records = []
input_file_path = "../files/sample_orders_transformed.json.gz"

# Different stores could have different timezones.
# OPTION1: Stores the date as isoformat with timezone information (e.g. "2018-03-01T00:00:00+00:00") -> Problem if reading the JSON from a language or system that do not offer compatibility with that format.
# OPTION2: Stores the dates in UTC (Universal Time Coordinated).

sample_timestamp = 1697044679
result = 1697037479

sample_timezone = pytz.timezone('Europe/Berlin')
print(sample_timezone)


def transform_to_utc(timezone, original_timestamp):
    original_date = timezone.localize(datetime.datetime.fromtimestamp(original_timestamp))
    print(original_date)
    return int(original_date.astimezone(pytz.UTC).timestamp())

#print(transform_to_utc(sample_timezone, sample_timestamp))

def test_transform_to_utc():
    utc_timestamp = transform_to_utc(sample_timezone, sample_timestamp)
    print(utc_timestamp)
    assert utc_timestamp == 1697037479

#test_transform_to_utc()
"""

if __name__ == "__main__":
    with gzip.open(input_file_path, 'rt', encoding='utf-8') as infile:
        for line in infile:
            record = json.loads(line)
            new_record = record
            local_tz = pytz.timezone(record['TIMEZONE'])
            print(local_tz)
            new_record['CREATED_AT_UTC'] = transform_to_utc(local_tz, record['CREATED_AT'])  # local_created_at.astimezone(pytz.UTC).isoformat()
            new_record['UPDATED_AT_UTC'] = transform_to_utc(local_tz, record['UPDATED_AT'])  # local_updated_at.astimezone(pytz.UTC).isoformat()
            #print(local_created_at.astimezone(pytz.UTC).isoformat())
            print(f"Original one: {record['CREATED_AT']}, new one:{new_record['CREATED_AT_UTC']}")
            print(f"Original one: {record['UPDATED_AT']}, new one:{new_record['UPDATED_AT_UTC']}")
            break
            records.append(new_record)
"""