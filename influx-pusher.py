from geoip2.database import Reader as GeoIPReader
from kafka import KafkaConsumer

mmdb = GeoIPReader('./db/GeoLite2-City.mmdb')
asndb = GeoIPReader('./db/GeoLite2-ASN.mmdb')

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('suricata',
                         group_id='mameaw14',
                         bootstrap_servers=['202.28.214.90:9092'])
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))