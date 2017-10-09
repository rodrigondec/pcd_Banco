from threading import Thread, Event
from time import sleep
from random import choice, randrange
from Banco import Banco
from Logger import Log
from Exceptions import SaldoException

class Pessoa(object):
    """pessoa"""
    count_pessoas = 0
    lista_pessoas = []
    log = Log('pessoa')

    @staticmethod
    def start():
        for pessoa in Pessoa.lista_pessoas:
            pessoa.t.start()

    def __init__(self):
        Pessoa.count_pessoas += 1
        self.id_pessoa = str(Pessoa.count_pessoas)
        Pessoa.lista_pessoas.append(self)
        Banco().criar_conta(self)

        self.dinheiro = 0
        self.triste = False

        self.vez = Event()
        self.vez.clear()

        self.uso_caixa = Event()
        self.uso_caixa.clear()

        self.t = Thread(target=self.viver, name=("Pessoa "+self.id_pessoa))

    def __str__(self):
        return "Pessoa "+self.id_pessoa

    def viver(self):
        while True:
            self.fazer_acao()
            sleep(5)

    def fazer_acao(self):
        acao = randrange(1, 4)
        if self.triste:
            acao = 2
        if acao == 1:
            self.gastar(randrange(10, 300, 10))
        elif acao == 2:
            self.trabalhar(randrange(10, 70, 10))
        elif acao == 3:
            self.transferir(randrange(50, 200, 50))

    def trabalhar(self, valor):
        Pessoa.log.info("vai trabalhar")
        sleep(5)
        Pessoa.log.info("ganhou "+str(valor))
        self.dinheiro += valor
        self.depositar()

    def gastar(self, valor):
        Pessoa.log.info("vai gastar " + str(valor))
        try:
            if self.dinheiro < valor:
                Pessoa.log.info("nao tem dinheiro vivo o suficiente. falta {}".format(valor-self.dinheiro))
                self.sacar(valor-self.dinheiro)
            Pessoa.log.info("gastou {}".format(valor))
        except SaldoException as e:
            Pessoa.log.info(e.message)
            self.triste = True

    def depositar(self):
        Pessoa.log.info("vai depositar {}".format(self.dinheiro))
        quantia = self.dinheiro
        Banco().depositar(self, self.dinheiro)
        self.dinheiro = 0
        Pessoa.log.info("depositou {}. Ela tem agora {} no banco. Ela esta satisfeita".format(quantia, Banco().saldo(self)))
        self.triste = False

    def sacar(self, valor):
        Pessoa.log.info("vai sacar "+str(valor))
        # try:
        Banco().sacar(self, valor)
        # except SaldoException as err:
        #     Pessoa.log.info(err.message)
            # self.triste = True
        Pessoa.log.info("sacou {}. Ela esta feliz :D".format(valor))

    def transferir(self, valor):
        pessoa_d = choice([pessoa for pessoa in Pessoa.lista_pessoas if pessoa != self])
        Pessoa.log.info("vai transferir "+str(valor)+" para Pessoa "+str(pessoa_d.id_pessoa))

        assert isinstance(pessoa_d, Pessoa)
        try:
            Banco().transferir(self.id_pessoa, pessoa_d.id_pessoa, valor)
            Pessoa.log.info("transferiu "+str(valor)+" para Pessoa "+str(pessoa_d.id_pessoa))
        except Exception:
            Pessoa.log.info("nao tem saldo o suficiente para trasnsferir. Ela esta triste :c")
            self.triste = True

    def get_id(self):
        return self.id_pessoa
