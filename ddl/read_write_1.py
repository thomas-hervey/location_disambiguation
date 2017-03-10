import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import json

with open('bernie_1.json') as json_data:
    d = json.load(json_data)

schema = avro.schema.parse(open("schema1.avsc", "rb").read())

writer = DataFileWriter(open("schema1.avro", "wb"), DatumWriter(), schema)
writer.append(d)
# writer.append({"name": "Alyssa", "favorite_number": 256})
# writer.append({"name": "Ben", "favorite_number": 7, "favorite_color": "red"})
writer.close()

reader = DataFileReader(open("schema1.avro", "rb"), DatumReader())
for user in reader:
    print user
reader.close()


# flicker key ad8ec1465d64040f51129b03e979dda3
# flicker secret b4bfb5e4c57967e5