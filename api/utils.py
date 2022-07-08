import json
import requests
import jq

def get_latest_csv_from_ckan(ckan_url,ckan_dataset):
    try:
        ckan_metadata = requests.get(f"{ckan_url}/api/3/action/package_show?id={ckan_dataset}")
        json_data = json.loads(ckan_metadata.text)
        ckan_resource = jq.compile("[ .result.resources[] | { name: .name, format: .format} ] | map(select(.format == \"CSV\")) | sort_by(.name) | reverse | .[0].name").input(json_data).first()
        return ckan_resource
    except Exception as e:
        print(f"An error occured fetching the latest resource for {ckan_dataset}: {e}")
        return None