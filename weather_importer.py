import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import os
from datetime import datetime

TZ = tz_string = datetime.now().astimezone().tzinfo


def import_weather_data() -> pd.DataFrame:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = os.getenv('meteo_url')
    params = {
        "latitude": os.getenv('lat'),
        "longitude": os.getenv('long'),
        "minutely_15": ["temperature_2m", "precipitation"],
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "cloud_cover"],
        "timezone": "auto",
        "forecast_hours": 24
    }
    responses = openmeteo.weather_api(url, params=params)
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    hourly_dataframe = extract_hourly_data(response)

    return hourly_dataframe


def extract_hourly_data(response):
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
    hourly_data = {"datetime_range": pd.date_range(start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                                         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                                         freq=pd.Timedelta(seconds=hourly.Interval()),
                                         inclusive="left"
                                         ),
                   "temperature_2m": hourly_temperature_2m,
                   "precipitation_probability": hourly_precipitation_probability,
                   "precipitation": hourly_precipitation,
                   "cloud_cover": hourly_cloud_cover}
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe['temperature_2m'] = hourly_dataframe['temperature_2m'].round(decimals=1)
    hourly_dataframe['local_time'] = hourly_dataframe['datetime_range']\
        .dt.tz_convert(TZ)\
        .dt.strftime("%H:%M")
    return hourly_dataframe


def extract_15minute_data(response):
    # Process minutely_15 data. The order of variables needs to be the same as requested.
    minutely_15 = response.Minutely15()
    minutely_15_temperature_2m = minutely_15.Variables(0).ValuesAsNumpy()
    minutely_15_precipitation = minutely_15.Variables(1).ValuesAsNumpy()
    minutely_15_data = {"date": pd.date_range(
        start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
        end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=minutely_15.Interval()),
        inclusive="left"
    ), "temperature_2m": minutely_15_temperature_2m, "precipitation": minutely_15_precipitation}
    minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)
    return minutely_15_dataframe
