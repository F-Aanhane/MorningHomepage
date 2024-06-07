import pandas as pd
import json
from datetime import datetime
import re
import dotenv


def open_json() -> pd.DataFrame:
    with open('example.json') as f:
        payload = json.load(f)['payload']
    departures = payload['departures']
    return pd.DataFrame(departures)


def prepare_data(deps: pd.DataFrame):
    deps[['planned', 'actual', 'delay']] = refactor_dt_cols(deps.actualDateTime, deps.plannedDateTime)
    deps = deps.drop(['name', 'product', 'plannedTimeZoneOffset',
                      'actualTimeZoneOffset', 'routeStations', 'departureStatus',
                      'actualDateTime', 'plannedDateTime'], axis=1)
    deps = deps[['trainCategory', 'direction', 'actual', 'planned', 'plannedTrack', 'actualTrack', 'messages']]
    return deps.to_html(index=False, border=0), deps.columns


def refactor_dt_cols(actual: pd.Series, planned: pd.Series):
    actual = pd.to_datetime(actual)
    planned = pd.to_datetime(planned)
    delay = actual - planned
    actual = actual.dt.strftime('%H:%M')
    planned = planned.dt.strftime('%H:%M')
    return pd.DataFrame({'planned': planned, 'actual': actual, 'delay': delay})


def run():
    deps = open_json()
    data, cols = prepare_data(deps)
    return data, cols
