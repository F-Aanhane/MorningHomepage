from pandas import DataFrame, Series, to_datetime
import json
import requests
import os
from enum import Enum


def get_response() -> dict:
    url = os.getenv('ns_url')

    payload = {}
    headers = {
        'Cache-Control': os.getenv('cache'),
        'Ocp-Apim-Subscription-Key': os.getenv('key')
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()


def data2prepared_html(data: dict) -> str:
    departures = data['payload']['departures']
    data = DataFrame(departures)
    data[['planned', 'actual', 'delay']] = refactor_dt_cols(data.actualDateTime, data.plannedDateTime)
    data = data \
        .drop(['name', 'product', 'plannedTimeZoneOffset', 'actualTimeZoneOffset', 'routeStations', 'departureStatus',
               'actualDateTime', 'plannedDateTime'], axis=1) \
        .rename({'trainCategory': 'cat', 'actualTrack': 'platform'}, axis=1)
    data['warnings'] = data['messages'].apply(extract_warning_message)
    data = data[['planned', 'delay', 'cat', 'direction', 'platform', 'warnings']]
    html = data.to_html(index=False, border=0)
    return html


def refactor_dt_cols(actual: Series, planned: Series) -> DataFrame:
    actual = to_datetime(actual)
    planned = to_datetime(planned)
    delay = '+' + (((actual - planned).dt.seconds / 60).astype(int)).astype(str)
    delay = delay.replace('+0', '')

    actual = actual.dt.strftime('%H:%M')
    planned = planned.dt.strftime('%H:%M')
    return DataFrame({'planned': planned, 'actual': actual, 'delay': delay})


def extract_warning_message(messages: list) -> str:
    warnings = '\n '.join(m['message'] for m in messages if m['style'] == MessageStyle.WARNING.value)
    return warnings


def open_example_json() -> dict:
    with open('example_ns.json') as f:
        data = json.load(f)
    return data


def run(debug: bool = False) -> str:
    if not debug:
        data = get_response()
    else:
        data = open_example_json()
    html = data2prepared_html(data)
    return html


class MessageStyle(Enum):
    WARNING = 'WARNING'
    INFO = 'INFO'
