import pandas as pd
import json
import requests
import os
from enum import Enum


def open_example_json(example_file) -> dict:
    with open(example_file) as f:
        payload = json.load(f)
    return payload


def get_payload_departures():
    response_json = get_response()
    payload = response_json['payload']
    departures = payload['departures']
    return departures


def get_response():
    url = os.getenv('ns_url')

    payload = {}
    headers = {
        'Cache-Control': os.getenv('cache'),
        'Ocp-Apim-Subscription-Key': os.getenv('key')
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def prepare_data(payload: dict) -> str:
    data = pd.DataFrame(payload)
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


def run(debug=False):
    if not debug:
        payload_ns = get_payload_departures()
    else:
        payload_ns = open_example_json('example_ns.json')
    ns = prepare_data(payload_ns)
    return ns


class MessageStyle(Enum):
    WARNING = 'WARNING'
    INFO = 'INFO'
