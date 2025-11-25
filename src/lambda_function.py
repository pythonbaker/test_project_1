import json
import requests


ARCGIS_URL = "https://spatial-gis.information.qld.gov.au/arcgis/rest/services/Basemaps/FoundationData/FeatureServer/0/query"
PARAMS = {
    'where': '1=1',
    'outFields': '*',
    'f': 'json',
    'resultRecordCount': 10
}


def getData(params):
    response = requests.get(ARCGIS_URL, params)
    data = response.json()
    # print(type(data)) -- dict
    # data_features = json.dumps(data['features'])
    # print(type(data_features)) -- string
    data_features = data['features']
    print(data_features)
    return data_features


getData(PARAMS)