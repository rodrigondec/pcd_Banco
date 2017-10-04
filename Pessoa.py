from threading import Thread
from time import sleep
from random import choice, randrange
from Banco import Banco
from Logger import Log

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
        Banco().criar_conta(self.id_pessoa)

        self.dinheiro = 0
        self.triste = False

        self.t = Thread(target=self.viver)

    def __str__(self):
        return "Pessoa "+self.id_pessoa

    def viver(self):
        while True:
            self.fazer_acao()
            sleep(5)

    def fazer_acao(self):
        acao = randrange(1, 3)
        if self.triste:
            acao = 2
        if acao == 1:
            self.gastar(randrange(10, 300, 10))
        elif acao == 2:
            self.trabalhar(randrange(10, 70, 10))
        elif acao == 3:
            self.transferir(randrange(50, 200, 50))

    def trabalhar(self, valor):
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " vai trabalhar")
        sleep(5)
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " ganhou "+str(valor))
        self.dinheiro += valor
        self.depositar()

    def gastar(self, valor):
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " vai gastar " + str(valor))
        try:
            if self.dinheiro < valor:
                Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " nao tem dinheiro vivo o suficiente. falta "+ str(valor-self.dinheiro))
                self.sacar(valor-self.dinheiro)
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " gastou " + str(valor))
        except Exception:
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " nao tem saldo. Tem so "+str(Banco().saldo(self.id_pessoa))+" para sacar. Ela esta triste :c")
            self.triste = True

    def depositar(self):
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " vai depositar " + str(self.dinheiro))
        quantia = self.dinheiro
        Banco().depositar(self.id_pessoa, self.dinheiro)
        self.dinheiro = 0
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " depositou " + str(quantia)+". Ela tem agora "+str(Banco().saldo(self.id_pessoa))+" no banco. Ela esta satisfeita")
        self.triste = False

    def sacar(self, valor):
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " pergunta, operacoes liberadas?")
        if not Banco().operacao_liberada.is_set():
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " espera operacoes liberaram")
            Banco().operacao_liberada.wait()
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " vai sacar "+str(valor))

        Banco().sacar(self.id_pessoa, valor)
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " sacou "+str(valor)+". Ela esta feliz :D")

    def transferir(self, valor):
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " pergunta, operacoes liberadas?")
        if not Banco().operacao_liberada.is_set():
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " espera operacoes liberaram")
            Banco().operacao_liberada.wait()
        pessoa_d = choice([pessoa for pessoa in Pessoa.lista_pessoas if pessoa != self])
        Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " vai transferir "+str(valor)+" para Pessoa "+str(pessoa_d.id_pessoa))

        assert isinstance(pessoa_d, Pessoa)
        try:
            Banco().transferir(self.id_pessoa, pessoa_d.id_pessoa, valor)
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " transferiu "+str(valor)+" para Pessoa "+str(pessoa_d.id_pessoa))
        except Exception:
            Pessoa.log.info("Pessoa " + str(self.id_pessoa) + " nao tem saldo o suficiente para trasnsferir. Ela esta triste :c")
            self.triste = True
