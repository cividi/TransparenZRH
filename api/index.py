from frictionless import Package, Layout, transform, steps
import requests
import datetime
import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


def air_layout_pipeline(sensor, url_Open_Data_Katalog):
    # sensor = 'Zch_Stampfenbachstrasse'
    filters = {"Standort": sensor}
    load_params = {'resource_id': '4466ec4a-b215-4134-8973-2f360e53c33d',
                   "sort": 'Datum desc',
                   "limit": 9,
                   "filters": json.dumps(filters)
                   }

    response = requests.get(url_Open_Data_Katalog, params=load_params)
    json_response = response.json()
    if 'result' in json_response.keys():
        json_results = json_response['result']
        if len(json_results) < 1:
            print('No results in response')
        if 'records' in json_results.keys():
            json_records = json_results['records']
            if len(json_records) < 1:
                print('No records in results')
        else:
            print('response.result not correct structure')
    else:
        print('response not correct structure')

    for entry in json_records:
        if entry['Parameter'] == 'NO2':
            NO2_unit, NO2_value, NO2_parameter, NO2_label = entry[
                'Einheit'], entry['Wert'], entry['Parameter'], 'Stickstoffdioxid (NO2)'
        if entry['Parameter'] == 'O3':
            O3_unit, O3_value, O3_parameter, O3_label = entry[
                'Einheit'], entry['Wert'], entry['Parameter'], 'Ozon (O3)'
        if entry['Parameter'] == 'PM10':
            PM10_unit, PM10_value, PM10_parameter, PM10_label = entry[
                'Einheit'], entry['Wert'], entry['Parameter'], 'Schwebestaub (PM10)'

    return Response(
        json.dumps({
            "layout": 'air',
            "sensor": sensor,
            "title": f"Luftqualität {sensor}",
            "description": "Die ersten systematischen Messungen der Luftqualität begannen in Zürich bereits Anfang der 1980er Jahre, weshalb wir auf eine der längsten Datenreihen der Schweiz zurückblicken können. Die Daten der Messtationen werden via OpenData-Portal im Internet zugänglich gemacht.",
            "updated": datetime.datetime.strptime(json_records[0]['Datum'], "%Y-%m-%dT%H:%M%z").isoformat(),
            "gauges": [
                {
                    "label": NO2_label,
                    "value": NO2_value,
                    "unit": NO2_unit
                },
                {
                    "label": O3_label,
                    "value": O3_value,
                    "unit": O3_unit
                },
                {
                    "label": PM10_label,
                    "value": PM10_value,
                    "unit": PM10_unit
                }
            ],
        },),
        mimetype='application/json',
        status=200)


def unknown_layout_pipeline(layout, sensor):
    return Response(
        json.dumps({
            "layout": layout,
            "sensor": sensor,
            "titel": "Unknown layout",
            "updated": datetime.datetime.now().isoformat(),
        },),
        mimetype='application/json',
        status=200)


@app.route('/api/v1/<string:layout>/<string:sensor>')
@cross_origin()
def api(layout, sensor):
    url_Open_Data_Katalog = "https://data.stadt-zuerich.ch/api/3/action/datastore_search?"

    if layout == 'air':
        return air_layout_pipeline(sensor, url_Open_Data_Katalog)
    else:
        return unknown_layout_pipeline(layout, sensor)
