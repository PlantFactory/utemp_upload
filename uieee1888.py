
import uxml
import urequests

FIAP_DATA_HEADERS = { "SOAPAction": "\"http://soap.fiap.org/data\"", "Content-Type": "text/xml charset=UTF-8" }


class IEEE1888:
    def __init__(self, fiap_url):
        self.fiap_url = fiap_url

    def write(self, data):
        if not isinstance(data, list):
            data = [data]

        builder = uxml.Builder()

        r = urequests.post(self.fiap_url, data=builder.build(self._build_write_request(data)), headers=FIAP_DATA_HEADERS)
        r.close()

        del builder

        return r.status_code

    def _build_write_request(self, data):
        fiap_data_template = { "Envelope": { "$": { "xmlns": "http://schemas.xmlsoap.org/soap/envelope/" }, "Body": { "dataRQ": { "$": { "xmlns": "http://soap.fiap.org/" }, "transport": { "$": { "xmlns": "http://gutp.jp/fiap/2009/11/" } } } } } }

        body_dict = { "point": [] }

        for row in data:
            body_dict["point"].append({ "$": { "id": row["id"] }, "value": { "$": { "time": row["time"] }, "_": row["value"] } })

        fiap_data_template["Envelope"]["Body"]["dataRQ"]["transport"]["body"] = body_dict

        return fiap_data_template
