from flask import Flask, render_template, session, request, jsonify
import geemap.foliumap as geemap
import ee
import json

app = Flask(__name__)
app.secret_key = '9d4e1e23bd5b727046a9e3b4b7db57bd8d6ee684'


DATASETS = {
        "Sentinel2": "COPERNICUS/S2_SR",
        "Landsat8": "LANDSAT/LC08/C02/T1_TOA",
        "SRTM": "CGIAR/SRTM90_V4",
        "WorldCover": "ESA/WorldCover/v100"
        }


@app.route('/', methods=['GET', 'POST'])
def index():
    Map = initialize_map()
    check_aoi()

    process_form_data(request)

    for image, vis_param, name in generate_map_layers():
        Map.addLayer(image, vis_param, name)

    map_html = Map.to_html(as_string=True)
    return render_template('index.html', map_html=map_html)


def initialize_map():
    Map = geemap.Map()
    try:
        Map.centerObject(ee.Geometry.Polygon(session['aoi']))
    except:
        pass
    return Map


@app.route('/capture-alert', methods=['POST'])
def capture_alert():
    data = request.json
    alert_message = json.loads(data.get('alertMessage'))
    session['aoi'] = alert_message['geometry']['coordinates']
    return jsonify({'status': 'success'})


@app.route('/reset-analysis', methods=['POST'])
def reset_analysis():
    session.clear()
    return jsonify({'status': 'success'})


def add_new_data(data, form_data):
    data.append(dict())
    last_layer_index = len(data) - 1
    if form_data['satellite'] == 'Sentinel2' or form_data['satellite'] == 'Landsat8':
        data[last_layer_index] = {
            "vis_params": {
                "bands": [form_data['band1'], form_data['band2'], form_data['band3']],
                "gamma": 2
            },
            "date": [form_data["minDate"], form_data["maxDate"]],
            "index": form_data["index"],
        }
    elif form_data['satellite'] == 'WorldCover':
        data[last_layer_index] = {
            "vis_params": {
                'bands': ['Map'],
            },
            "index": ""
        }
    else:
        data[last_layer_index] = {
            "vis_params": {},
            "index": "",
        }
    data[last_layer_index]["source"] = DATASETS[form_data['satellite']]
    data[last_layer_index]["name"] = f"Layer {last_layer_index} {form_data['name']}"
    return data


def compute_ndvi(nir, red):
    return nir.subtract(red).divide(nir.add(red))


def compute_ndwi(green, nir):
    return green.subtract(nir).divide(nir.add(green))


def compute_rvi(nir, red):
    return nir.divide(red)


index_functions = {
    'NDVI': {'func': compute_ndvi, 'vis': {'min': -1, 'max': 1, 'palette': ["blue", "white", "green"]}},
    'NDWI': {'func': compute_ndwi, 'vis': {'min': -1, 'max': 1, 'palette': ["red", "yellow", "blue"]}},
    'RVI': {'func': compute_rvi, 'vis': {'min': -1, 'max': 1, 'palette': ["red", "yellow", "blue"]}},
}


def generate_map_layers():
    for image, vis_param, name, index, source in generate_layer_data(session['data']):
        nir = image.select("B5") if source == DATASETS["Landsat8"] else image.select("B8")
        green = image.select("B3")
        red = image.select("B4")

        if index in index_functions:
            vis_param = index_functions[index]['vis']
            image = index_functions[index]['func'](nir if index != 'NDWI' else green, red)

        yield image, vis_param, name


def check_aoi():
    if 'aoi' not in session:
        session['aoi'] = [[[19.792042, 50.016344], [19.792042, 50.096468], [20.050564, 50.096468], [20.050564, 50.016344], [19.792042, 50.016344]]]


def process_form_data(request):
    if request.method == 'POST':
        optional_fields = ['name', 'satellite', 'index', 'band1', 'band2', 'band3', 'min', 'max', 'minDate', 'maxDate']
        data = {field: request.form.get(field) if request.form.get(field) is not None else "" for field in optional_fields}

    try:
        session['data'] = add_new_data(session['data'], data) if 'data' in session else []
    except:
        pass


def generate_layer_data(data):
    for warstwa in data:
        collection = ee.ImageCollection(warstwa['source']) if warstwa['source'] in {DATASETS["Landsat8"], DATASETS["Sentinel2"], DATASETS["WorldCover"]} else ee.Image(warstwa['source'])

        if 'date' in warstwa:
            collection = collection.filterDate(warstwa['date'][0], warstwa['date'][1])

        if warstwa['source'] in [DATASETS["Landsat8"], DATASETS["Sentinel2"], DATASETS["WorldCover"]]:
            collection = collection.filterBounds(ee.Geometry.Polygon(session['aoi']))

        if warstwa['source'] == DATASETS["Sentinel2"]:
            collection = collection.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)).first()
        elif warstwa['source'] == DATASETS["Landsat8"]:
            collection = collection.filter(ee.Filter.lt('CLOUD_COVER', 10)).min()
        elif warstwa['source'] == DATASETS["WorldCover"]:
            collection = collection.first()

        image = collection.clip(ee.Geometry.Polygon(session['aoi']))

        if warstwa["index"] == "":
            stats = image.reduceRegion(
                reducer=ee.Reducer.minMax(),
                geometry=ee.Geometry.Polygon(session['aoi']),
                scale=30,
                maxPixels=1e9
            )

            min_max_values = stats.getInfo()
            if warstwa["source"] == DATASETS["Landsat8"] or warstwa['source'] == DATASETS["Sentinel2"]:
                warstwa['vis_params']['min'] = [min_max_values[f'{band}_min'] for band in warstwa['vis_params']['bands']]
                warstwa['vis_params']['max'] = [min_max_values[f'{band}_max'] for band in warstwa['vis_params']['bands']]
            elif warstwa["source"] == DATASETS["SRTM"]:
                warstwa['vis_params']['min'] = min_max_values['elevation_min']
                warstwa['vis_params']['max'] = min_max_values['elevation_max']

        yield image, warstwa['vis_params'], warstwa['name'], warstwa["index"], warstwa["source"]


if __name__ == '__main__':
    app.run(debug=True)
