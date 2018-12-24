from flask import Flask
from flask_restful import Resource, Api, reqparse
from influxdb import InfluxDBClient

app = Flask(__name__)
api = Api(app)

client = InfluxDBClient('localhost', 8086, '', '', 'suricata')

class Index(Resource):
    def get(self):
        return {'message': 'OK'}

class List(Resource):
    def get(self):
        result = client.query('select * from ids;')
        print(result)
        print(type(result))
        return result



api.add_resource(Index, '/')
api.add_resource(List, '/list')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8014)
