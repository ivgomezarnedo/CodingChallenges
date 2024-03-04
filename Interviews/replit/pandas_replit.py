import pandas as pd
ot_hist_df = pd.read_json('ot-hist.txt', lines=True)
print(ot_hist_df.head())

ot_hist_df['total_ops'] = ot_hist_df['ops'].apply(len)
print(ot_hist_df.head())

def count_operations_by_type(line, op_type):
    count = 0
    for op in line:
        if list(op['Op'].keys())[0] == op_type:
            count += 1
    return count

distinct_ops = set()
for opers in ot_hist_df['ops'].values:
    for op in opers:
        distinct_ops.add(list(op['Op'].keys())[0])
print(distinct_ops)

for op_type in distinct_ops:
    ot_hist_df[f'{op_type.lower()}_ops'] = ot_hist_df['ops'].apply(lambda x: count_operations_by_type(x, op_type))
print(ot_hist_df.head())

pd.set_option('display.max_columns', None)
print(ot_hist_df.head())

ot_hist_df['seconds_elapsed'] = ot_hist_df['committed'].apply(lambda x: x['seconds']-min_seconds)
# Sum all operations by seconds elapsed

# Order dataframe by seconds in descending order
ot_hist_df = ot_hist_df.sort_values(by='seconds', ascending=True)

# Get seconds into another column
ot_hist_df['seconds'] = ot_hist_df['committed'].apply(lambda x: x['seconds'])
ot_hist_df['nanos'] = ot_hist_df['committed'].apply(lambda x: x['seconds']*1000000000 + x['nanos'])

# Filter dataframe based on nanos
ot_hist_df = ot_hist_df[ot_hist_df['nanos'] > 0]

# Create a time-series plot showing the number of ops over time by op type using previous dataframe with a certain x_limit
ot_hist_df.plot(x='seconds', y=['total_ops', 'insert_ops', 'update_ops', 'delete_ops'], kind='line')
ot_hist_df.plot(x='seconds', y=['insert_ops', 'update_ops', 'delete_ops'])

import matplotlib.pyplot as plt
ot_hist_df.plot(x='minutes_elapsed', y=['delete_ops', 'skip_ops', 'insert_ops'])
plt.show()

# Create a time-series plot showing the number of ops over range time by op type using previous dataframe
ot_hist_df.plot(x='minutes_elapsed', y=['delete_ops', 'skip_ops', 'insert_ops'], kind='area')


# Using previous dataframe calculate number of ops per second or minute
#ot_hist_df['ops_per_second'] = ot_hist_df['total_ops'] / ot_hist_df['seconds']
#ot_hist_df['ops_per_minute'] = ot_hist_df['total_ops'] / (ot_hist_df['seconds']/60)

# Using previous dataframe get the number of all operations
total_ops = ot_hist_df['total_ops'].sum()

# Group by CRC and calculate the average number of operations
ot_hist_df_grouped = ot_hist_df.groupby('crc32')['total_ops'].mean()
# """


# Write a function that returns the document as of a specific point in time using previous dataframe. The function should take in a date/time and return the document contents as of that time


def apply_bundle_operation(bundle_operation, document):
    cursor = 0
    for entry in bundle_operation:
        operation = entry['Op']
        op_type = list(operation.keys())[0]
        if op_type == 'Skip':
            cursor = cursor + operation[op_type]
        elif op_type == 'Delete':
            document = document[:cursor]+document[cursor+operation[op_type]:]
        elif op_type == 'Insert':
            document = document[:cursor]+operation[op_type]+document[cursor:]
            cursor = cursor + len(operation[op_type])
    return document

document = ""
def get_document_at_time(time_ns, df):
    df = df[df['nanos'] <= time_ns].sort_values(by='nanos', ascending=True)
    document = ""
    for bundle_operation in df['ops'].values:
        document = apply_bundle_operation(bundle_operation, document)
    return document


ot_hist_df = ot_hist_df.sort_values(by=['seconds', 'nanos'], ascending=True)
total_opers = []
for oper_list in ot_hist_df['ops'].values:
    total_opers.append(oper_list)
apply_operation(document, cursor, ot_hist_df['ops'].values[0])


# Order dataframe by seconds and nanos in descending order
ot_hist_df = ot_hist_df.sort_values(by=['seconds', 'nanos'], ascending=False)

import streamlit as st

from datetime import datetime

start_time = st.slider(
     "When do you start?",
     value=datetime.fromtimestamp(1633731010601741473 // 1000000000),
     min_value=datetime.fromtimestamp(1633731010601741473 // 1000000000),
     max_value=datetime.fromtimestamp(1638568185373755184 // 1000000000),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)






