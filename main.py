from flask import Flask, request, render_template, Markup
import ns_importer
import weather_importer
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__
            , template_folder='templates'
            , static_folder='static'
            , static_url_path='/')

DEBUG = os.getenv('debug')


@app.route('/')
def index():
    if request.method == 'GET':
        labels, markup_departures, precipitation, precipitation_probability, temperature, cloud_cover = extract_data()

        return render_template('base.html'
                               , departures=markup_departures
                               , temperature=temperature
                               , precipitation=precipitation
                               , precipitation_probability=precipitation_probability
                               , cloud_cover=cloud_cover
                               , labels=labels)


def extract_data():
    departures = ns_importer.run()
    if DEBUG:
        with open('test_departures.html', 'w') as h:
            h.write(departures)
    weather_data = weather_importer.import_weather_data()

    markedup_departures = Markup(departures)
    labels = weather_data.date.dt.strftime("%H:%M").to_list()
    precipitation = weather_data.precipitation.to_list()
    temperature = weather_data.temperature_2m.to_list()
    temperature = [round(n, 1) for n in temperature]
    precipitation_probability = weather_data.precipitation_probability.to_list()
    cloud_cover = weather_data.cloud_cover.to_list()

    return labels, markedup_departures, precipitation, precipitation_probability, temperature, cloud_cover


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=DEBUG)
