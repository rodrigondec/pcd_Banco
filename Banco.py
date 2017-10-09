from threading import Thread
from Logger import Log
from time import sleep
from Caixa import Caixa
from Conta import Conta
from Exceptions import TransfException


class Banco(object):
    """banco"""
    log = Log("banco")
    qt_caixas = 1


    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance.init()
        return type._instance

    def init(self):
        for _ in range(0, Banco.qt_caixas):
            Caixa()

        self.t = Thread(target=self.investimento, name='Banco_Investimento')
        self.t.start()

    def __str__(self):
        return "Banco"

    def investimento(self):
        sleep(10)
        while True:
            try:
                Banco.log.info("investimento iniciando")
                for id_pessoa, conta  in Conta.contas.items():
                    conta.lock.acquire()

                sleep(5)

                for id_pessoa, conta in Conta.contas.items():
                    conta.depositar(conta.saldo()/10)
                Banco.log.info("investimento terminado")
            finally:
                for id_pessoa, conta  in Conta.contas.items():
                    conta.lock.release()

            sleep(15)

    def criar_conta(self, pessoa):
        Conta(pessoa.get_id())

    def saldo(self, pessoa):
        return Conta.ver_saldo(pessoa.get_id())

    def sacar(self, pessoa, valor):
        self._entrar_fila(pessoa)
        Conta.realizar_saque(pessoa.get_id(), valor)

    def depositar(self, pessoa, valor):
        self._entrar_fila(pessoa)
        Conta.realizar_deposito(pessoa.get_id(), valor)

    def transferir(self, pessoa_o, pessoa_d, valor):
        self._entrar_fila(pessoa_o)
        conta_o = Conta.get_conta(pessoa_o.get_id())
        conta_d = Conta.get_conta(pessoa_d.get_id())

        try:
            conta_o.lock.acquire()
            conta_d.lock.acquire()

            saldo_o_antes = conta_o.saldo()
            saldo_d_antes = conta_d.saldo()

            conta_o.sacar(valor)
            conta_d.depositar(valor)

            if conta_o.saldo() != (saldo_o_antes-valor) or conta_d.saldo() != (saldo_d_antes+valor):
                conta_o.dinheiro = saldo_o_antes
                conta_d.dinheiro = saldo_d_antes
                raise TransfException()
        finally:
            conta_o.lock.release()
            conta_d.lock.release()

    def _entrar_fila(self, pessoa):
        type(pessoa).log.info("entrou na fila do banco")
        Caixa.fila.put(pessoa)
        if not pessoa.vez.is_set():
            type(pessoa).log.info("espera sua vez")
            pessoa.vez.wait()
