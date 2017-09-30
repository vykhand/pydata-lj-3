import os
import logging
from flask import Flask, render_template

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
log = logging.getLogger()

app = Flask(__name__)

if "SERVER_ADDRESS" not in os.environ:
    log.error("SERVER_ADDRESS environment variable is not set. Setting to 0.0.0.0")
    server.address = "0.0.0.0"
else:
    server_address = os.environ["SERVER_ADDRESS"]

def modify_doc(doc):
    df = sea_surface_temperature.copy()
    source = ColumnDataSource(data=df)

    plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
                  title="Sea Surface Temperature at 43.18, -70.43")
    plot.line('time', 'temperature', source=source)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            data = df.rolling('{0}D'.format(new)).mean()
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=30, value=0, step=1, title="Smoothing by N Days")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yaml")

bkapp = Application(FunctionHandler(modify_doc))

@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://{}:5006/bkapp'.format(server_address))
    return render_template("embed.html", script=script, template="Flask")

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp},address="0.0.0.0", allow_websocket_origin=["0.0.0.0:8000","localhost:8000","localhost:5006", "0.0.0.0:5006", "pydata3app.azurewebsites.net:8000", "pydata3app.azurewebsites.net:80", "pydata3app.azurewebsites.net:5060"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    log.addHandler(logging.StreamHandler(stream=sys.stdout))
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(host='0.0.0.0', port=8000)
