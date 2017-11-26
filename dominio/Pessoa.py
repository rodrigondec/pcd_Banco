from random import choice, randrange
from threading import Thread, Event
from time import sleep

from sckt.SocketBroker import SocketBroker
from rmi.RMIClientBroker import RMIClientBroker
from rest.RestBroker import RestBroker

from dominio.Logger import Log
from dominio.Operacao import Deposito, Saque, Transferencia


class Pessoa(object):
    """pessoa"""
    count_pessoas = 0
    lista_pessoas = []
    log = Log('pessoa')

    @staticmethod
    def start():
        for pessoa in Pessoa.lista_pessoas:
            pessoa.thread.start()

    def __init__(self):
        if self.__class__ is Pessoa:
            raise TypeError('abstract class cannot be instantiated')
        Pessoa.count_pessoas += 1
        self.id_pessoa = str(Pessoa.count_pessoas)
        Pessoa.lista_pessoas.append(self)

        self.dinheiro = 0
        self.triste = False

        self.thread = Thread(target=self.viver, name=self)

    def __str__(self):
        return "{} {}".format(type(self).__name__ ,self.id_pessoa)

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
        if self.dinheiro < valor:
            Pessoa.log.info("nao tem dinheiro vivo o suficiente. falta {}".format(valor-self.dinheiro))
            self.sacar(valor-self.dinheiro)
        self.dinheiro = 0
        Pessoa.log.info("gastou {}".format(valor))

    def realizar_operacao(self, operacao):
        raise NotImplementedError

    def depositar(self):
        Pessoa.log.info("vai depositar {}".format(self.dinheiro))
        quantia = self.dinheiro
        resp = self.realizar_operacao(Deposito(self.get_id(), quantia))
        self.dinheiro = 0
        Pessoa.log.info("depositou {}. Ela tem agora {} no banco."
                        " Ela esta satisfeita".format(quantia, resp['msg']))
        self.triste = False

    def sacar(self, valor):
        Pessoa.log.info("vai sacar "+str(valor))
        resp = self.realizar_operacao(Saque(self.get_id(), valor))
        if resp['status']:
            Pessoa.log.info("sacou {}. Ela esta feliz :D".format(valor))
        else:
            Pessoa.log.info("{}. Ela esta triste :c".format(resp['msg']))
            self.triste = True

    def transferir(self, valor):
        pessoa_d = choice(self._get_lista_pessoa())
        Pessoa.log.info("vai transferir {} para Pessoa {}".format(valor, pessoa_d))

        assert isinstance(pessoa_d, Pessoa)
        resp = self.realizar_operacao(Transferencia(self.get_id(), valor, pessoa_d.get_id()))
        if resp['status']:
            Pessoa.log.info("transferiu {} para Pessoa {}".format(valor, pessoa_d))
        else:
            Pessoa.log.info("{}. Ela esta triste :c".format(resp['msg']))
            self.triste = True

    def _get_lista_pessoa(self):
        return [pessoa for pessoa in Pessoa.lista_pessoas if pessoa != self and not isinstance(pessoa, Dependente)]

    def get_id(self):
        return self.id_pessoa


class Dependente(Pessoa):
    """Pessoa dependente"""

    def __init__(self):
        self.responsavel = choice([pessoa for pessoa in Pessoa.lista_pessoas if not isinstance(pessoa, Dependente)])
        Pessoa.__init__(self)

    def __str__(self):
        return "{} {}, dependente de {}".format(type(self).__name__, self.id_pessoa, self.responsavel.id_pessoa)

    def _get_lista_pessoa(self):
        return [pessoa for pessoa in Pessoa.lista_pessoas if not isinstance(pessoa, Dependente) and pessoa != self.responsavel]

    def get_id(self):
        return self.responsavel.id_pessoa


class PessoaSocket(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketBroker(operacao).execute()


class DependenteSocket(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return SocketBroker(operacao).execute()


class PessoaRMI(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return RMIClientBroker(operacao).execute()


class DependenteRMI(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return RMIClientBroker(operacao).execute()


class PessoaRest(Pessoa):
    def __init__(self):
        Pessoa.__init__(self)

    def realizar_operacao(self, operacao):
        return RestBroker(operacao).execute()


class DependenteRest(Dependente):
    def __init__(self):
        Dependente.__init__(self)

    def realizar_operacao(self, operacao):
        return RestBroker(operacao).execute()

