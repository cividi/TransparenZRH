import datetime
from dateutil import parser
import urllib
import locale
import json
import yaml
import decimal
import requests
from flask import Flask, Response
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import Headers

from frictionless import Pipeline
from jinja2 import Environment, FileSystemLoader

from .utils import get_latest_csv_from_ckan

locale.setlocale(locale.LC_ALL, "de_DE")

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@app.route("/api/v2/<string:layout>/<string:sensor>")
@cross_origin()
def api(layout, sensor):
    ckan_url = "https://data.stadt-zuerich.ch"
    response_body = {}
    response_code = 500

    sensor = urllib.parse.unquote(sensor, encoding="utf-8", errors="replace")

    if layout == "air":
        ckan_dataset = "ugz_luftschadstoffmessung_stundenwerte"
        ckan_resource = get_latest_csv_from_ckan(ckan_url, ckan_dataset)
        data = {
            "ckan_url": ckan_url,
            "ckan_resource": ckan_resource,
            "sensor_name": sensor.replace("Zch_", ""),
            "sensor_id": sensor,
            "date_field": "Datum",
        }
    elif layout == "camera":
        sensor_name = (
            "Wohnsiedlung Hardau II" if sensor == "Hardau" else "- unbekannte Kamera"
        )
        data = {
            "date": datetime.datetime.now().isoformat(),
            "sensor_name": sensor_name,
            "sensor_id": sensor,
            "date_field": "date",
        }
    elif layout == "car":
        data = {
            "sensor_id": sensor,
            "date_field": "DATZEIT",
        }
    elif layout == "bike" or layout == "pedestrian":
        try:
            ckan_dataset = "ted_taz_verkehrszaehlungen_werte_fussgaenger_velo"
            ckan_resource = get_latest_csv_from_ckan(ckan_url, ckan_dataset)
            r = requests.head(
                f"{ckan_url}/dataset/{ckan_dataset}/download/{ckan_resource}"
            )
            source_time = parser.parse(r.headers["last-modified"])
        except Exception as e:
            raise Exception(f"{e}, couldn't parse datetime string.")
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
            env = Environment(loader=FileSystemLoader("api/descriptors"))
            template = env.get_template(f"{layout}.pipeline.yaml")
            recipe = template.render(params=data)
            target = Pipeline(yaml.full_load(recipe)).run()

            pkg = target.task.target

            if not target.valid:
                print(target)

            # inline the data for serialization
            for resource in pkg.resource_names:
                pkg.get_resource(resource).data = pkg.get_resource(resource).to_inline(
                    dialect=dict(keyed=True)
                )
                if data["date_field"] in pkg.get_resource(resource).schema.field_names:
                    pkg["created"] = pkg.get_resource(resource).data[0][
                        data["date_field"]
                    ]

            response_body = pkg
            response_code = 200
        except Exception as e:
            response_body = dict(error=f"An internal error occured: {e}")
            response_code = 200

    return Response(
        json.dumps(response_body, cls=DecimalEncoder),
        mimetype="application/json",
        status=response_code,
        headers=Headers(
            [("Cache-Control", "max-age=0, s-maxage=60, stale-while-revalidate=86400")]
        ),
    )
