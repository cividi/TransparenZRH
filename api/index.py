import requests
import datetime
from dateutil import parser
import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


def get_verkehrszaehlungs_sensor_id(abkuerzung):
    url = 'https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Standorte_der_automatischen_Fuss__und_Velozaehlungen?service=WFS&version=1.1.0&request=GetFeature&outputFormat=GeoJSON&typename=view_eco_standorte'
    response = requests.get(url)
    json_response = response.json()
    for entry in json_response.get('features', {}):
        properties = entry.get('properties', {})
        if properties.get('abkuerzung', '') == abkuerzung and properties.get('bis', abkuerzung) is None:
            name = properties.get('bezeichnung', abkuerzung)
            fk_zaehler = properties.get('fk_zaehler', abkuerzung)
    return {"name": name, "fk_zaehler": fk_zaehler}


def camera_layout_pipeline(sensor, url_Open_Data_Katalog):

    layout = {
        "layout": 'bike',
        "sensor": sensor,
        "title": f"Videoüberwachung – unbekannte Kamera",
        "description": "Die angegebene Kamera konnte nicht gefunden werden.",
        "updated": datetime.datetime.now().isoformat(),
        "gauges": [],
        "links": [],
    }

    if sensor == "Hardau_II":
        layout["title"] = "Videoüberwachung Wohnsiedlung Hardau II"
        layout["description"] = ""
        layout["gauges"] = [
            {
                "label": 'Standort',
                "value": 'Hardau II',
                "unit": 'Wohnsiedlung',
            },
            {
                "label": 'Aufbewahrungsdauer',
                "value": 7,
                "unit": 'Tage',
            },
            {
                "label": 'Was wird überwacht?',
                "value": 'Lifte',
                "unit": 'Innenbereich',
            },
            {
                "label": 'Verantwortliche Dienstabteilung',
                "value": 'LSZ',
                "unit": 'Liegenschaften Stadt Zürich'
            }]

    return Response(
        json.dumps(layout),
        mimetype='application/json',
        status=200)


def counter_layout_pipeline(sensor_, url_Open_Data_Katalog, type_):
    no_value = 'n.v.'
    sensor = get_verkehrszaehlungs_sensor_id(sensor_)

    layout = {
        "layout": '',
        "sensor": sensor['name'],
        "title": type_,
        "description": '',
        "updated": '',
        "gauges": [],
        "links": []
    }

    filters = {"FK_ZAEHLER": sensor['fk_zaehler']}
    if type_ == "bike":
        unit = "Velos"
        fields = ['VELO_IN', 'VELO_OUT', 'DATUM']
        layout["title"] = f"Velozählstelle {sensor['name']} ({sensor_})"
        layout['description'] = "Das Tiefbauamt der Stadt Zürich erhebt seit 2009 die Velofrequenzen in der Stadt Zürich mit Hilfe automatischer Zählgeräte. Das Zählstellennetz umfasst derzeit 24 Zählgeräte. Die Messung erfolgt über im Boden eingelassene Induktionsschlaufen. Über Funk werden die Daten an einen Server übermittelt. Die Geräte sind vor dem Hintergrund des Datenschutzes unbedenklich, da lediglich Velofahrten gezählt und keine Daten über Nutzer oder Velos detektiert werden können. Die Daten der Zählgeräte werden via OpenData-Portal im Internet frei zugänglich gemacht."
        layout["links"] = [
            {
                "url": "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/resource/ebe5e78c-a99f-4607-bedc-051f33d75318",
                "text": "Rohdaten auf data.stadt-zuerich.ch"
            },
            {
                "url": "https://www.stadt-zuerich.ch/ted/de/index/taz/verkehr/webartikel/webartikel_velozaehlungen.html",
                "text": "Weitere Informationen und Daten zu Velozählungen in der Stadt Zürich"
            },
            {
                "url": "http://www.opendefinition.org/licenses/cc-zero",
                "text": "Creative Commons CCZero Lizenz"
            }]
    else:
        unit = "Personen"
        fields = ['FUSS_IN', 'FUSS_OUT', 'DATUM']
        layout["title"] = f"Fussgängerzählstelle {sensor['name']} ({sensor_})"
        layout["description"] = "Seit 2013 werden die Frequenzen des Fussverkehrs automatisch erfasst. Derzeit sind 18 Zählgeräte in Betrieb. Die Frequenzen des Fussverkehrs werden von den Zählgeräten mittels passiver Infrarotstrahlung erhoben. Die damit erhobenen Daten bilden eine wichtige quantitative Grundlage zur Beurteilung der Entwicklung des Fussverkehrs auf dem Stadtgebiet. Die Daten der Zählgeräte werden via OpenData-Portal im Internet zugänglich gemacht."
        layout["links"] = [
            {
                "url": "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/resource/ebe5e78c-a99f-4607-bedc-051f33d75318",
                "text": "Rohdaten auf data.stadt-zuerich.ch"
            },
            {
                "url": "https://www.stadt-zuerich.ch/ted/de/index/taz/verkehr/webartikel/webartikel_fussverkehrszaehlung.html",
                "text": "Weitere Informationen und Daten zu Fussgängerzählungen in der Stadt Zürich"
            },
            {
                "url": "http://www.opendefinition.org/licenses/cc-zero",
                "text": "Creative Commons CCZero Lizenz"
            }
        ]

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
        if type_ == "bike":
            in_, out_ = entry['VELO_IN'], entry['VELO_OUT']
        else:
            in_, out_ = entry['FUSS_IN'], entry['FUSS_OUT']
        if type(in_) != str:
            in_ = 0
        if type(out_) != str:
            out_ = 0
        if entrys_date == yesterday:
            counter_yesterday += int(in_) + int(out_)
        if entrys_date == today:
            counter_today += int(in_) + int(out_)
        list_of_all_counts.append(int(in_) + int(out_))

    counter_year = sum(list_of_all_counts)
    if len(list_of_all_counts) > 0:
        mean_per_15Min_over_all = sum(
            list_of_all_counts)/len(list_of_all_counts)
        mean_per_day = int(mean_per_15Min_over_all * 24 * 60 / 15)
    else:
        mean_per_day = no_value

    if counter_today == 0:
        counter_today = no_value
    if counter_yesterday == 0:
        counter_yesterday = no_value
    if counter_year == 0:
        counter_year = no_value

    layout["updated"] = datetime.datetime.strptime(
        json_records[-1]['DATUM'], "%Y-%m-%dT%H:%M").isoformat()

    layout["gauges"] = [
        {
            "label": 'Gestern',
            "value": counter_yesterday,
            "unit": unit
        },
        {
            "label": 'Tagesdurchschnitt',
            "value": mean_per_day,
            "unit": unit
        },
        {
            "label": 'Seit Jahresbeginn',
            "value": counter_year,
            "unit": unit
        },
        {
            "label": 'Heute',
            "value": counter_today,
            "unit": unit
        }
    ]

    return Response(
        json.dumps(layout),
        mimetype='application/json',
        status=200)


def air_layout_pipeline(sensor, url_Open_Data_Katalog):
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
                },
                {
                    "url": "https://www.stadt-zuerich.ch/gud/de/index/umwelt_energie/luftqualitaet/messdaten.html",
                    "text": "Weitere Informationen und Daten zur Luftqualitätsmessung in der Stadt Zürich"
                },
                {
                    "url": "http://www.opendefinition.org/licenses/cc-zero",
                    "text": "Creative Commons CCZero Lizenz"
                }
            ]
        },),
        mimetype='application/json',
        status=200)


def unknown_layout_pipeline(layout, sensor):
    return Response(
        json.dumps({
            "layout": layout,
            "sensor": sensor,
            "title": "unknown",
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
        return counter_layout_pipeline(sensor, url_Open_Data_Katalog, 'bike')
    elif layout == 'pedestrian':
        return counter_layout_pipeline(sensor, url_Open_Data_Katalog, 'pedestrian')
    elif layout == 'camera':
        return camera_layout_pipeline(sensor, url_Open_Data_Katalog)
    else:
        return unknown_layout_pipeline(layout, sensor)
