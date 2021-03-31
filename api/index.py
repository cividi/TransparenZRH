import json
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)


@app.route('/api/v1/<string:layout>/<string:sensor>')
@app.route('/api/v1', defaults={'layout': '', 'sensor': ''})
@cross_origin()
def api(layout, sensor):
    return Response(
        json.dumps({
            "dataset": layout,
            "time": sensor,
        },),
        mimetype='application/json',
        status=200)
