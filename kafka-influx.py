from geoip2.database import Reader as GeoIPReader
from kafka import KafkaConsumer
import json
from influxdb import InfluxDBClient

mmdb = GeoIPReader('./db/GeoLite2-City.mmdb')
asndb = GeoIPReader('./db/GeoLite2-ASN.mmdb')

consumer = KafkaConsumer('suricata',
                 group_id='oh_my_gosh',
                 bootstrap_servers=['202.28.214.90:9092'],
		enable_auto_commit=False)
client = InfluxDBClient('localhost', 8086, '', '', 'suricata')

def flatten(current, key, result):
    if isinstance(current, dict):
        for k in current:
            new_key = "{0}_{1}".format(key, k) if len(key) > 0 else k
            flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    # print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
        #                                  message.offset, message.key,
        #                                 message.value))

        data = json.loads(message.value)
        try:
                res = mmdb.city(data['dest_ip'])
                asn = asndb.asn(data['dest_ip'])
                data['dest_latitude'] = res.location.latitude
                data['dest_longitude'] = res.location.longitude
                data['dest_country_name'] = res.country.names['en']
                data['dest_asn'] = asn.autonomous_system_number
                data['dest_autonomous_system'] = asn.autonomous_system_organization
        except:
                data['dest_latitude'] = 0.0
                data['dest_longitude'] = 0.0
                data['dest_country_name'] = 'unknown'
                data['dest_asn'] = 'unknown'
                data['dest_autonomous_system'] = 'unknown'
        try:
                res = mmdb.city(data['src_ip'])
                asn = asndb.asn(data['src_ip'])
                data['src_latitude'] = res.location.latitude
                data['src_longitude'] = res.location.longitude
                data['src_country_name'] = res.country.names['en']
                data['src_asn'] = asn.autonomous_system_number
                data['src_autonomous_system'] = asn.autonomous_system_organization
        except:
                data['src_latitude'] = 0.0
                data['src_longitude'] = 0.0
                data['src_country_name'] = 'unknown'
                data['src_asn'] = 'unknown'
                data['src_autonomous_system'] = 'unknown'

        json_body = [{
                "measurement":"intrusion",
                "time":data['timestamp'],
		"tags":flatten(data,'',{}),
                "fields":flatten(data,'',{})
        }]
        print(json_body)
        client.write_points(json_body)
