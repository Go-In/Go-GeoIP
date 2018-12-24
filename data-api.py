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
        result = client.query('SELECT * FROM ids ORDER BY time DESC LIMIT 20;')
        return list(result.get_points())

class Stat(Resource):
    def get(self):
        src_ip = client.query('SELECT FIRST("src_ip"), COUNT("src_ip") FROM "ids" GROUP BY "src_ip";')
        dest_ip = client.query('SELECT FIRST("dest_ip"), COUNT("dest_ip") FROM "ids" GROUP BY "dest_ip";')
        src_country_name = client.query('SELECT FIRST("src_country_name"), COUNT("src_country_name") FROM "ids" GROUP BY "src_country_name";')
        dest_country_name = client.query('SELECT FIRST("dest_country_name"), COUNT("dest_country_name") FROM "ids" GROUP BY "dest_country_name";')

        return {
            "src_ip":list(src_ip.get_points()),
            "dest_ip":list(dest_ip.get_points()),
            "src_country":list(src_country_name.get_points()),
            "dest_country":list(dest_country_name.get_points())
        }

api.add_resource(Index, '/')
api.add_resource(List, '/list')
api.add_resource(Stat, '/stat')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8014)
