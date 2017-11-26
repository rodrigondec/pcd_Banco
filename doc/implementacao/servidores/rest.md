# Rest

## Server

O servidor rest foi implementado utilizando as bibliotecas [Flask](http://flask.pocoo.org/) e [Flask-Restplus](https://flask-restplus.readthedocs.io/en/stable/) [Socket](https://docs.python.org/3/library/socket.html). Ele recebe uma operação em formato json que foi serializada manualmente e depois manda a operação para ser executada no singleton do Banco, retornando o valor da execução da operação para o cliente.

### Código

```py
def StartRestServer():
    RestServer.run(host="localhost", port=REST_PORT, debug=False)


RestServer = Flask(__name__) # create the application instance :)
RestServer.config.from_object(__name__) # load config from this file , flaskr.py
# Define Api application object
RestServerAPI = Api(RestServer, version='1.0', title='pdc_Banco',
description='API rest do pdc_Banco',)

# Define the blueprint: 'core', set its url prefix: RestServer.url/core
mod_core = Blueprint('core', __name__, url_prefix='core/')
ns_core = Namespace('core', 'Core da API')

op_fields = ns_core.model('op_fields', {
    "id_pessoa": fields.String,
    "valor": fields.Integer
})

op_expect = ns_core.model('operacao',{
    "classe": fields.String,
    "objeto": fields.Nested(op_fields)
})

resp_m = ns_core.model('resposta',{
    'status': fields.Boolean,
    'msg': fields.String
})


@ns_core.route('/realizar_operacao/')
class OperacaoController(Resource):
    @ns_core.expect(op_expect)
    @ns_core.marshal_with(resp_m)
    @ns_core.response(200, 'Operação realizada')
    def post(self):
        """Realiza uma operação"""
        data = request.json

        operacao = None
        if data['classe'] == "Saldo":
            operacao = Saldo(data['objeto']['id_pessoa'])
        elif data['classe'] == "Deposito":
            operacao = Deposito(data['objeto']['id_pessoa'], data['objeto']['valor'])
        elif data['classe'] == "Saque":
            operacao = Saque(data['objeto']['id_pessoa'], data['objeto']['valor'])
        elif data['classe'] == "Transferencia":
            operacao = Transferencia(data['objeto']['id_pessoa'], data['objeto']['valor'], data['objeto']['id_pessoa_d'])

        resp = {}
        try:
            resp['status'] = True
            resp['msg'] = Banco().realizar_operacao(operacao)
        except SaldoException as e:
            resp['status'] = False
            resp['msg'] = e.message

        return resp

RestServer.register_blueprint(mod_core)
RestServerAPI.add_namespace(ns_core)
```

---

## RestClientBroker

O cliente PessoaRest e DependenteRest utilizam a classe RestClientBroker para realizar a comunicação com o servidor rest. E será nela que terá a o request https utilizando a biblioteca [Request](http://docs.python-requests.org/en/master/), juntamente com a serialização da operação e desserialização da resposta.

### Código

```py
class RestClientBroker:
    def __init__(self, operacao):
        self.operacao = operacao

    def execute(self):
        data = json.dumps(self.operacao.toJson())

        url = "http://localhost:{}/core/realizar_operacao/".format(REST_PORT)
        headers = {'Content-Type': 'application/json', "Accept": "application/json"}

        resp = requests.post(url, data=data, headers=headers)

        return resp.json()
```



