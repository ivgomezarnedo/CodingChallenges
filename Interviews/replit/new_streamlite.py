import streamlit as st

from datetime import datetime
import pandas as pd
from dateutil import parser


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

def get_document_at_time(time_ns):
    ot_hist_df = pd.read_json('ot-hist.txt', lines=True)
    ot_hist_df['nanos'] = ot_hist_df['committed'].apply(lambda x: x['seconds'] * 1000000000 + x['nanos'])
    ot_hist_df = ot_hist_df[ot_hist_df['nanos'] <= time_ns].sort_values(by='nanos', ascending=True)
    document = ""
    for bundle_operation in ot_hist_df['ops'].values:
        document = apply_bundle_operation(bundle_operation, document)
    return document

def get_max_nanos_ts():
    ot_hist_df = pd.read_json('ot-hist.txt', lines=True)
    ot_hist_df['nanos'] = ot_hist_df['committed'].apply(lambda x: x['seconds'] * 1000000000 + x['nanos'])
    max_nanos_ts = ot_hist_df['nanos'].max()
    return max_nanos_ts

def get_min_nanos_ts():
    ot_hist_df = pd.read_json('ot-hist.txt', lines=True)
    ot_hist_df['nanos'] = ot_hist_df['committed'].apply(lambda x: x['seconds'] * 1000000000 + x['nanos'])
    min_nanos_ts = ot_hist_df['nanos'].min()
    return min_nanos_ts

def date_to_nanos(date):
    nanos_date = date.timestamp() * 1000000000
    return nanos_date

start_time = st.slider(
     "When do you start?",
     value=datetime.fromtimestamp(get_min_nanos_ts() // 1000000000),
     min_value=datetime.fromtimestamp(get_min_nanos_ts() // 1000000000),
     max_value=datetime.fromtimestamp(get_max_nanos_ts() // 1000000000),
     format="MM/DD/YY - hh:mm:ss")
st.write("Start time:", get_document_at_time(date_to_nanos(start_time)))
