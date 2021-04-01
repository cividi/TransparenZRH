from frictionless import Package, Layout, transform, steps
import requests
import datetime
from dateutil import parser
import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


def get_name_for_verkehrszaehlungs_sensor_id(FK_ZAEHLER):
    url = 'https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Standorte_der_automatischen_Fuss__und_Velozaehlungen?service=WFS&version=1.1.0&request=GetFeature&outputFormat=GeoJSON&typename=view_eco_standorte'
    response = requests.get(url)
    json_response = response.json()
    for entry in json_response.get('features', {}):
        properties = entry.get('properties', {})
        if properties.get('fk_zaehler', '') == FK_ZAEHLER:
            name = properties.get('bezeichnung', FK_ZAEHLER)
    return name


def bike_layout_pipeline(sensor, url_Open_Data_Katalog):
    filters = {"FK_ZAEHLER": sensor}
    fields = ['VELO_IN', 'VELO_OUT', 'DATUM']
    load_params = {'resource_id': 'ebe5e78c-a99f-4607-bedc-051f33d75318',
                   'fields': ', '.join(fields),
                   'filters': json.dumps(filters),
                   'limit': 32000,
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

    counter_today, counter_yesterday, list_of_all_counts = 0, 0, []
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    for entry in json_records:
        entrys_date = parser.isoparse(entry['DATUM']).date()
        velo_in, velo_out = entry['VELO_IN'], entry['VELO_OUT']
        if type(velo_in) != str:
            velo_in = 0
        if type(velo_out) != str:
            velo_out = 0
        if entrys_date == yesterday:
            counter_yesterday += int(velo_in) + int(velo_out)
        if entrys_date == today:
            counter_today += int(velo_in) + int(velo_out)
        list_of_all_counts.append(int(velo_in) + int(velo_out))

    counter_year = sum(list_of_all_counts)
    if len(list_of_all_counts) > 0:
        mean_per_15Min_over_all = sum(
            list_of_all_counts)/len(list_of_all_counts)
        mean_per_day = int(mean_per_15Min_over_all * 24 * 60 / 15)
    else:
        mean_per_day = 'Kann zZt. noch nicht dargestellt werden.'

    if counter_today == 0:
        counter_today = 'Kann zZt. noch nicht dargestellt werden.'
    if counter_yesterday == 0:
        counter_yesterday = 'Kann zZt. noch nicht dargestellt werden.'
    if counter_year == 0:
        counter_year = 'Kann zZt. noch nicht dargestellt werden.'
    sensor_name = get_name_for_verkehrszaehlungs_sensor_id(sensor)
    return Response(
        json.dumps({
            "layout": 'bike',
            "sensor": sensor,
            "title": f"Velozählstelle  {sensor_name} ({sensor})",
            "description": "Das Tiefbauamt der Stadt Zürich erhebt seit 2009 die Velofrequenzen in der Stadt Zürich mit Hilfe automatischer Zählgeräte. Das Zählstellennetz umfasst derzeit 24 Zählgeräte. Die Messung erfolgt über im Boden eingelassene Induktionsschlaufen. Über Funk werden die Daten an einen Server übermittelt. Die Geräte sind vor dem Hintergrund des Datenschutzes unbedenklich, da lediglich Velofahrten gezählt und keine Daten über Nutzer oder Velos detektiert werden können. Die Daten der Zählgeräte werden via OpenData-Portal im Internet frei zugänglich gemacht.",
            "updated": datetime.datetime.strptime(json_records[-1]['DATUM'], "%Y-%m-%dT%H:%M").isoformat(),
            "gauges": [
                {
                    "label": 'Anzahl Velos gestern',
                    "value": counter_yesterday,
                    "unit": ''
                },
                {
                    "label": 'Durchschnittliche Velos pro Tag',
                    "value": mean_per_day,
                    "unit": ''
                },
                {
                    "label": 'Total Velos seit Jahresbeginn',
                    "value": counter_year,
                    "unit": ''
                },
                {
                    "label": 'Anzahl Velos heute',
                    "value": counter_today,
                    "unit": ''
                }
            ],
            "links": [
                {
                    "url": "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/resource/ebe5e78c-a99f-4607-bedc-051f33d75318",
                    "text": "Rohdaten auf data.stadt-zuerich.ch"
                }]
        },),
        mimetype='application/json',
        status=200)


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
            "title": f"Luftqualität {sensor.replace('Zch_','')}",
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
            "links": [
                {
                    "url": "https://data.stadt-zuerich.ch/dataset/ugz_luftschadstoffmessung_stundenwerte/resource/4466ec4a-b215-4134-8973-2f360e53c33d",
                    "text": "Rohdaten auf data.stadt-zuerich.ch"
                }]
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
    elif layout == 'bike':
        return bike_layout_pipeline(sensor, url_Open_Data_Katalog)
    else:
        return unknown_layout_pipeline(layout, sensor)
