import pandas as pd
import json
import re
# import dotenv
from enum import Enum


def open_json(example) -> pd.DataFrame:
    with open(example) as f:
        payload = get_ns_payload(f)
    return pd.DataFrame(payload)


def get_ns_payload(f):
    payload = json.load(f)['payload']
    departures = payload['departures']
    return departures


def prepare_data(data: pd.DataFrame) -> str:
    data[['planned', 'actual', 'delay']] = refactor_dt_cols(data.actualDateTime, data.plannedDateTime)
    data = data \
        .drop(['name', 'product', 'plannedTimeZoneOffset', 'actualTimeZoneOffset', 'routeStations', 'departureStatus',
               'actualDateTime', 'plannedDateTime'], axis=1) \
        .rename({'trainCategory': 'cat', 'actualTrack': 'platform'}, axis=1)
    data['warnings'] = data['messages'].apply(extract_warning)
    data = data[['planned', 'delay', 'cat', 'direction', 'platform', 'warnings']]
    html = data.to_html(index=False, border=0)   # , col_space={'planned': 0, 'delay': 0}
    return html


def refactor_dt_cols(actual: pd.Series, planned: pd.Series):
    actual = pd.to_datetime(actual)
    planned = pd.to_datetime(planned)
    delay = '+' + (((actual - planned).dt.seconds / 60).astype(int)).astype(str)
    delay = delay.replace('+0', '')

    actual = actual.dt.strftime('%H:%M')
    planned = planned.dt.strftime('%H:%M')
    return pd.DataFrame({'planned': planned, 'actual': actual, 'delay': delay})


def extract_warning(x):
    return '\n '.join(m['message'] for m in x if m['style'] == MessageStyle.WARNING.value)


def run():
    payload_ns = open_json('example_ns.json')
    ns = prepare_data(payload_ns)
    return ns


class MessageStyle(Enum):
    WARNING = 'WARNING'
    INFO = 'INFO'
