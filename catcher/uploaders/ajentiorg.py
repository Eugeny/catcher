from base64 import b64encode
import requests
import zlib


class AjentiOrgUploader:
    def upload(self, data):
        return requests.post(
            'http://ajenti.org/catcher/submit',
            data={'text': b64encode(zlib.compress(data.encode('utf-8')))}
        ).text
