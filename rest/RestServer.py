from flask import Flask, Blueprint, request
from flask_restplus import Api, Namespace, fields, Resource

from dominio.Banco import Banco
from dominio.Exceptions import SaldoException
from dominio.Operacao import Saldo, Deposito, Saque, Transferencia

from config import REST_PORT


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

