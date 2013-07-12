import requests


class PasteHTMLUploader:
    def upload(self, data):
        return requests.post(
            'http://pastehtml.com/upload/create?input_type=html&result=address',
            data={'txt': data}
        ).text
