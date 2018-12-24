from flask import Flask
from flask_restful import Resource, Api, reqparse
from influxdb import InfluxDBClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)

CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

client = InfluxDBClient('localhost', 8086, '', '', 'suricata')

class Index(Resource):
    def get(self):
        return {'message': 'OK'}

class List(Resource):
    def get(self):
        result = client.query('select * from ids;')
        return list(result.get_points())



#api.add_resource(Index, '/')
api.add_resource(List, '/list')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8014)
