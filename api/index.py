from frictionless import Package, Layout, transform, steps
import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


@app.route('/api/v1/<string:layout>/<string:sensor>')
@app.route('/api/v1', defaults={'layout': 'bike', 'sensor': '2997'})
@cross_origin()
def api(layout, sensor):
    return Response(
        json.dumps({
            "layout": layout,
            "time": sensor,
            "titel": "Sensor Titel.",
            "description": "Sensor Beschreibungstext.",
            "updated": "2021-03-31T12:00",
            "gauges": [
                {
                    "label": "Seit Mitternacht",
                    "value": "20'342",
                    "unit": "Personen"
                },
                {
                    "label": "NOx",
                    "value": 12.1,
                    "unit": "m/s"
                },
                {
                    "label": "NO",
                    "value": 23.2,
                    "unit": "m/s"
                },
                {
                    "label": "Heute",
                    "value": "n.v.",
                    "unit": ""
                }
            ],
        },),
        mimetype='application/json',
        status=200)
