from uieee1888 import IEEE1888

client = IEEE1888("http://ants.jga.kisarazu.ac.jp/axis2/services/FIAPStorage")

client.write([{ "id": "http://mp-test/1", "time": "2018-05-08T04:11:55", "value": "1234" }])
