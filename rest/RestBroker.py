import requests
import json
from config import REST_PORT


class RestBroker:
    def __init__(self, operacao):
        self.operacao = operacao

    def execute(self):
        data = json.dumps(self.operacao.toJson())

        url = "http://localhost:{}/core/realizar_operacao/".format(REST_PORT)
        headers = {'Content-Type': 'application/json', "Accept": "application/json"}

        resp = requests.post(url, data=data, headers=headers)

        return resp.json()
