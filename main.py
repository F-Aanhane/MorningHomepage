import flask
import data_importer


app = flask.Flask(__name__
                  , template_folder='templates'
                  , static_folder='static'
                  , static_url_path='/')

@app.route('/')
def index():
    if flask.request.method == 'GET':
        departures, cols = data_importer.run()
        marked_departures = flask.Markup(departures)
        return flask.render_template('base.html', departures=marked_departures, message='no session data')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
