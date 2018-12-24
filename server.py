from flask import Flask
from flask_restful import Resource, Api, reqparse
from geoip2.database import Reader as GeoIPReader

mmdb = GeoIPReader('./db/GeoLite2-City.mmdb')
asndb = GeoIPReader('./db/GeoLite2-ASN.mmdb')

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return {'message': 'OK'}

class GeoIP(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ip',type=str, location='args')
        args = parser.parse_args()
        try:
            res = mmdb.city(args['ip'])
            asn = asndb.asn(args['ip'])
        except :
            return {
            'latitude': '0',
            'longitude': '0',
            'country_name': 'unknown',
            'asn': 'unknown',
            'autonomous_system': 'unknown'
            }
        
        return {
            'latitude': res.location.latitude,
            'longitude': res.location.longitude,
            'country_name': res.country.names['en'],
            'asn': asn.autonomous_system_number,
            'autonomous_system': asn.autonomous_system_organization
        }

api.add_resource(Index, '/')
api.add_resource(GeoIP, '/geo-ip')
if __name__ == '__main__':
    app.run(debug=True)
