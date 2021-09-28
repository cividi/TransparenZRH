import requests
import datetime
from dateutil import parser
import locale
import json
import yaml
from flask import Flask, Response
from flask_cors import CORS, cross_origin

from frictionless import Pipeline, steps, transform, Package, Resource
from jinja2 import Environment, FileSystemLoader

locale.setlocale(locale.LC_ALL, 'en_US')

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)

def get_verkehrszaehlungs_sensor_id(abkuerzung):
    sensors = transform(
        "api/descriptors/standorte-automatische-fuss-und-velozaehlungen.resource.yaml",
        steps = [
            steps.row_filter(formula="bis is None"),
            steps.field_remove(names=["bis"]),
            steps.row_filter(formula=f"abkuerzung == '{abkuerzung}'"),
            steps.field_update(name="bezeichnung", new_name="name"),
            steps.field_update(name="abkuerzung", new_name="sensor_ref"),
            steps.field_update(name="fk_zaehler", new_name="sensor_id"),
        ]
    )
    try:
        data = sensors.to_inline(dialect=dict(keyed=True))[0]
    except:
        data = {'sensor_ref': abkuerzung, 'name': '', 'sensor_id': ''}
    return data


def counter_layout_pipeline(sensor_, url_Open_Data_Katalog, type_):
    no_value = 'n.v.'
    sensor = get_verkehrszaehlungs_sensor_id(sensor_)

    filters = {"FK_ZAEHLER": sensor['sensor_id']}
    pkg = Package()

    if type_ == "bike":
        unit = "Velos"
        fields = ['VELO_IN', 'VELO_OUT', 'DATUM']
        
        pkg.title = f"Velozählstelle {sensor['name']} ({sensor_})"
        pkg.description = "Das Tiefbauamt der Stadt Zürich erhebt seit 2009 die Velofrequenzen in der Stadt Zürich mit Hilfe automatischer Zählgeräte. Das Zählstellennetz umfasst derzeit 24 Zählgeräte. Die Messung erfolgt über im Boden eingelassene Induktionsschlaufen. Über Funk werden die Daten an einen Server übermittelt. Die Geräte sind vor dem Hintergrund des Datenschutzes unbedenklich, da lediglich Velofahrten gezählt und keine Daten über Nutzer oder Velos detektiert werden können. Die Daten der Zählgeräte werden via OpenData-Portal im Internet frei zugänglich gemacht."
        pkg.sources = [
            {
                "path": "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/resource/ebe5e78c-a99f-4607-bedc-051f33d75318",
                "title": "Rohdaten auf data.stadt-zuerich.ch"
            },
            {
                "path": "https://www.stadt-zuerich.ch/ted/de/index/taz/verkehr/webartikel/webartikel_velozaehlungen.html",
                "title": "Weitere Informationen und Daten zu Velozählungen in der Stadt Zürich"
            },
            {
                "path": "http://www.opendefinition.org/licenses/cc-zero",
                "title": "Creative Commons CCZero Lizenz"
            }]
    else:
        unit = "Personen"
        fields = ['FUSS_IN', 'FUSS_OUT', 'DATUM']
        pkg.title = f"Fussgängerzählstelle {sensor['name']} ({sensor_})"
        pkg.description = "Seit 2013 werden die Frequenzen des Fussverkehrs automatisch erfasst. Derzeit sind 18 Zählgeräte in Betrieb. Die Frequenzen des Fussverkehrs werden von den Zählgeräten mittels passiver Infrarotstrahlung erhoben. Die damit erhobenen Daten bilden eine wichtige quantitative Grundlage zur Beurteilung der Entwicklung des Fussverkehrs auf dem Stadtgebiet. Die Daten der Zählgeräte werden via OpenData-Portal im Internet zugänglich gemacht."
        pkg.sources = [
            {
                "path": "https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/resource/ebe5e78c-a99f-4607-bedc-051f33d75318",
                "title": "Rohdaten auf data.stadt-zuerich.ch"
            },
            {
                "path": "https://www.stadt-zuerich.ch/ted/de/index/taz/verkehr/webartikel/webartikel_fussverkehrszaehlung.html",
                "title": "Weitere Informationen und Daten zu Fussgängerzählungen in der Stadt Zürich"
            },
            {
                "path": "http://www.opendefinition.org/licenses/cc-zero",
                "title": "Creative Commons CCZero Lizenz"
            }
        ]

    load_params = {'resource_id': 'ebe5e78c-a99f-4607-bedc-051f33d75318',
                   'fields': ', '.join(fields),
                   'sort': 'DATUM asc',
                   'filters': json.dumps(filters),
                   'limit': 32000,
                   'include_total': False
                   }

    pkg["views"] = [
        {
            "name": "gauge_view_1",
            "resources": ["data"],
            "specType": "gauge",
            "spec": {
                "mark": "number",
                "filter": { "field": "key", "equals": "sum_yesterday" },
                "encoding": { "label": "Gestern", "value": { "field": "value", "type": "quantitative" }, "unit": unit }
            }
        },
        {
            "name": "gauge_view_2",
            "resources": ["data"],
            "specType": "gauge",
            "spec": {
                "mark": "number",
                "filter": { "field": "key", "equals": "mean_day_year" },
                "encoding": { "label": "Tagesdurchschnitt seit Jahresbeginn", "value": { "field": "value", "type": "quantitative" }, "unit": unit }
            }
        },
        {
            "name": "gauge_view_3",
            "resources": ["data"],
            "specType": "gauge",
            "spec": {
                "mark": "number",
                "filter": { "field": "key", "equals": "sum_year" },
                "encoding": { "label": "Seit Jahresbeginn", "value": { "field": "value", "type": "quantitative" }, "unit": unit }
            }
        },
        {
            "name": "gauge_view_4",
            "resources": ["data"],
            "specType": "gauge",
            "spec": {
                "mark": "number",
                "filter": { "field": "key", "equals": "mean_seven_days" },
                "encoding": { "label": "Tagesdurchschnitt letzte 7 Tage", "value": { "field": "value", "type": "quantitative" }, "unit": unit }
            }
        }
    ]

    pkg.licenses = [
        {
            "title": "Creative Commons CCZero Lizenz",
            "name": "CC0",
            "path": "http://www.opendefinition.org/licenses/cc-zero"
        }
    ]

    response = requests.get(f"{url_Open_Data_Katalog}/api/3/action/datastore_search?", params=load_params)
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

    counter_today, counter_yesterday, seven_days, list_of_all_counts = 0, 0, [], []
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    lastweek = today - datetime.timedelta(days=7)
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
        if entrys_date >= lastweek:
            seven_days.append(int(in_) + int(out_))
        list_of_all_counts.append(int(in_) + int(out_))

    counter_year = sum(list_of_all_counts)
    if len(list_of_all_counts) > 0:
        mean_per_15Min_over_all = sum(
            list_of_all_counts)/len(list_of_all_counts)
        mean_per_day = int(mean_per_15Min_over_all * 24 * 60 / 15)
    else:
        mean_per_day = no_value

    if len(seven_days) > 0:
        mean_per_15Min_rolling = sum(
            seven_days)/len(seven_days)
        mean_rolling = int(mean_per_15Min_rolling * 24 * 60 / 15)
    else:
        mean_rolling = no_value

    if counter_today == 0:
        counter_today = no_value
    if counter_yesterday == 0:
        counter_yesterday = no_value
    if counter_year == 0:
        counter_year = no_value

    date = datetime.datetime.strptime(
        json_records[-1]['DATUM'], "%Y-%m-%dT%H:%M").isoformat()

    gauges_data = Resource(
        name = "data",
        data = [
            {
                "key": 'sum_yesterday',
                "value": counter_yesterday,
                "date": date,
            },
            {
                "key": 'mean_day_year',
                "value": mean_per_day,
                "date": date,
            },
            {
                "key": 'sum_year',
                "value": counter_year,
                "date": date,
            },
            {
                "key": 'mean_seven_days',
                "value": mean_rolling,
                "date": date,
            }
        ]
    )

    pkg["created"] = date

    pkg.add_resource(gauges_data)

    return (pkg, 200)

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
