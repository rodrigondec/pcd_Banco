from threading import Thread, Event
from Logger import Log
from time import sleep
from Caixa import Caixa
from Conta import Conta

class Banco(object):
    """banco"""
    log = Log("banco")

    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance.init()
        return type._instance

    def init(self):
        self.contas = {}

        self.dinheiro_investimento = Event()
        self.dinheiro_investimento.clear()

        self.operacao_liberada = Event()
        self.operacao_liberada.set()

        self.t = Thread(target=self.investimento, name='Banco_Investimento')
        # self.t.start()

    def __str__(self):
        return "Banco"

    def investimento(self):
        while True:
            Banco.log.info("pergunta, tenho dinheiro pra investir?")
            if not self.dinheiro_investimento.is_set():
                Banco.log.info("esperando condicao para investir")
                Banco().dinheiro_investimento.wait()
            with self.l_dinheiro:

                Banco.log.info("investindo o dinheiro dos clientes. Bloqueando operacoes de saque e "
                                "transferencia")
                self.operacao_liberada.clear()

                self.dinheiro = 0
                for id_pessoa, valor in self.clientes.items():
                    self.clientes[id_pessoa] = 0
                    self.clientes_investimento[id_pessoa] = valor

                sleep(8)

                for id_pessoa, valor in self.clientes_investimento.items():
                    self.dinheiro += valor + valor / 10
                    self.clientes[id_pessoa] += valor + valor / 10
                    self.clientes_investimento[id_pessoa] = 0

                Banco.log.info("terminou de investir")
                self.operacao_liberada.set()

            sleep(15)

    def criar_conta(self, id_pessoa):
        self.contas[id_pessoa] = Conta(id_pessoa)

    def saldo(self, id_pessoa):
        return self.clientes[id_pessoa]

    def verif_saldo_suf(self, id_pessoa, valor):
        if self.saldo(id_pessoa) < valor:
            raise Exception('Saldo Insuficiente!')
        return True

    def sacar(self, id_pessoa, valor):
        self.verif_saldo_suf(id_pessoa, valor)
        with self.l_dinheiro:
            self.clientes[id_pessoa] -= valor
            self.dinheiro -= valor
            Banco.log.info("deu " + str(valor) + " para a Pessoa " + str(id_pessoa) + ". Ele tem agora " + str(
                self.dinheiro))
            if self.dinheiro < 100:
                self.dinheiro_investimento.clear()
        return valor

    def depositar(self, id_pessoa, valor):
        with self.l_dinheiro:
            self.clientes[id_pessoa] += valor
            self.dinheiro += valor
            Banco.log.info("recebeu "+str(valor)+" da Pessoa "+str(id_pessoa)+". Ele tem agora "+str(self.dinheiro))
            if self.dinheiro >= 100:
                self.dinheiro_investimento.set()
        return True

    def transferir(self, id_pessoa_o, id_pessoa_d, valor):
        self.verif_saldo_suf(id_pessoa_o, valor)
        with self.l_dinheiro:
            self.sacar(id_pessoa_o, valor)
            self.depositar(id_pessoa_d, valor)
        return valor
