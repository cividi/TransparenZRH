import datetime
import locale
import json
import yaml
from flask import Flask, Response
from flask_cors import CORS, cross_origin

from frictionless import Pipeline
from jinja2 import Environment, FileSystemLoader

from api.lv_counter import *

locale.setlocale(locale.LC_ALL, 'en_US')

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)

@app.route('/api/v2/<string:layout>/<string:sensor>')
@cross_origin()
def api(layout, sensor):
    ckan_url = "https://data.stadt-zuerich.ch"
    response_body = {}
    response_code = 500

    if layout == 'air':
        data = {
            "ckan_url": ckan_url,
            "sensor_name": sensor.replace('Zch_',''),
            "sensor_id": sensor,
            "date_field": "Datum",
        }
    elif layout == 'camera':
        sensor_name = "Wohnsiedlung Hardau II" if sensor == "Hardau" else "- unbekannte Kamera"
        data = {
            "date": datetime.datetime.now().isoformat(),
            "sensor_name": sensor_name,
            "sensor_id": sensor,
            "date_field": "date",
        }
    elif layout == 'car':
        data = {
            "date": datetime.datetime.now().isoformat(),
            "sensor_name": sensor,
            "sensor_id": sensor,
            "date_field": "date",
        }
    elif layout == 'bike' or layout == 'pedestrian':
        response_body, response_code = counter_layout_pipeline(sensor, ckan_url, layout)
    else:
        layout = "unknown"
        data = {
            "date": datetime.datetime.now().isoformat(),
            "sensor_name": "unbekannt",
            "sensor_id": sensor,
            "date_field": "date",
        }

    if response_body == {} and response_code == 500:
        try:
            env = Environment(loader=FileSystemLoader('api/descriptors'))
            template = env.get_template(f"{layout}.pipeline.yaml")
            recipe = template.render(params = data)
            target = Pipeline(yaml.safe_load(recipe)).run()

            pkg = target.task.target

            # inline the data for serialization
            inline_data = pkg.get_resource("data").to_inline(dialect=dict(keyed=True))
            pkg.get_resource("data").data = inline_data
            pkg["created"] = inline_data[0][data["date_field"]]
            
            response_body = pkg
            response_code = 200
        except Exception as e:
            response_body = dict(
                error = f"An internal error occured: {e}"
            )
            response_code = 200

    return Response(
        json.dumps(response_body,),
        mimetype = 'application/json',
        status = response_code,
    )
