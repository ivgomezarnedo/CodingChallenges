import json
import gzip
import datetime
import pytz
records = []
input_file_path = "../files/sample_orders_transformed.json.gz"

# Outliers or wrong values in total_price
# OPTION1: Remove them or replace them by a default value -> We would lose data.
# OPTION2: Calculate the total based on the items and shipping price (Doing this we will calculate again the calculated field 'Total_price')
# OPTION3: If the price of the items also contains outliers or wrong values.
#   -> Ask for thresholds (MAX_TOTAL_PRICE) -> Raise alerts!
#   -> Calculate how far away a data point is from the mean in terms of standard deviations
if __name__ == "__main__":
    with gzip.open(input_file_path, 'rt', encoding='utf-8') as infile:
        for line in infile:
            record = json.loads(line)
            new_record = record
            calculated_total = round(sum(float(item['price']) for item in record['ITEMS']) + record['TOTAL_SHIPPING'],2) # Rounding it as original data.
            if record['TOTAL_PRICE'] is None or abs(record['TOTAL_PRICE'] != calculated_total):
                print(f"Wrong value identified for ID {record['ID']}. Original TOTAL_PRICE: {record['TOTAL_PRICE']}, Corrected TOTAL_PRICE: {calculated_total}")
                record['TOTAL_PRICE'] = calculated_total
            records.append(new_record)