import datetime
import locale
import json
import yaml
import decimal
import requests
from flask import Flask, Response
from flask_cors import CORS, cross_origin

from frictionless import Pipeline
from jinja2 import Environment, FileSystemLoader

locale.setlocale(locale.LC_ALL, 'en_US')

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

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
            "sensor_id": sensor,
            "date_field": "DATZEIT",
        }
    elif layout == 'bike' or layout == 'pedestrian':
        r = requests.head("https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/download/2021_verkehrszaehlungen_werte_fussgaenger_velo.csv")
        source_time = datetime.datetime.strptime(r.headers['last-modified'],
            #Fri, 27 Mar 2015 08:05:42 GMT
            '%a, %d %b %Y %X %Z')
        data = {
            "date": source_time.isoformat(),
            "sensor_ref": sensor,
            "date_field": "date",
        }
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
            target = Pipeline(yaml.full_load(recipe)).run()

            pkg = target.task.target

            if not target.valid:
                print(target)

            # inline the data for serialization
            for resource in pkg.resource_names:
                pkg.get_resource(resource).data = pkg.get_resource(resource).to_inline(dialect=dict(keyed=True))
                if data["date_field"] in pkg.get_resource(resource).schema.field_names:
                    pkg["created"] = pkg.get_resource(resource).data[0][data["date_field"]]
            
            response_body = pkg
            response_code = 200
        except Exception as e:
            response_body = dict(
                error = f"An internal error occured: {e}"
            )
            response_code = 200

    return Response(
        json.dumps(response_body, cls=DecimalEncoder),
        mimetype = 'application/json',
        status = response_code,
    )
