from flask import Flask, request, render_template, Markup
import ns_importer
import pandas as pd
import weather_importer

app = Flask(__name__
                  , template_folder='templates'
                  , static_folder='static'
                  , static_url_path='/')


@app.route('/')
def index():
    if request.method == 'GET':
        departures = ns_importer.run()
        weather_data = weather_importer.import_weather_data()
        with open('test.html', 'w') as h:
            h.write(departures)
        markedup_departures = Markup(departures)
        # markedup_weather = Markup(weather)
        labels = weather_data.date.dt.strftime("%H:%M").to_list()
        precipitation = weather_data.precipitation.to_list()
        precipitation_probability = weather_data.precipitation_probability.div(100).to_list()
        temperature = weather_data.temperature_2m.to_list()

        return render_template('base.html'
                               , departures=markedup_departures
                               , temperature=temperature
                               , precipitation=precipitation
                               , precipitation_probability=precipitation_probability
                               , labels=labels)
        # return render_template('base.html', departures=markedup_departures)

# Root endpoint 
@app.route('/chart')
def chart():
    if request.method == 'GET':
        departures = ns_importer.run()
        weather_data = weather_importer.import_weather_data()
        with open('test.html', 'w') as h:
            h.write(departures)
        markedup_departures = Markup(departures)
        # markedup_weather = Markup(weather)
        labels = weather_data.date.dt.strftime("%H:%M").to_list()
        precipitation = weather_data.precipitation.to_list()
        precipitation_probability = weather_data.precipitation_probability.div(100).to_list()
        temperature = weather_data.temperature_2m.to_list()

        return render_template('chart.html'
                               , departures=markedup_departures
                               , temperature=temperature
                               , precipitation=precipitation
                               , precipitation_probability=precipitation_probability
                               , labels=labels)
        # return render_template('base.html', departures=markedup_departures)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
    # weather_importer.import_weather_data()