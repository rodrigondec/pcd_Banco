from time import sleep
from random import choice
from Banco import Banco


class Pessoa(object):
    """pessoa"""
    count_pessoas = 0
    lista_pessoas = []

    def __init__(self):
        Pessoa.count_pessoas += 1
        self.id_pessoa = Pessoa.count_pessoas
        Pessoa.lista_pessoas.append(self)
        Banco().criar_conta(self.id_pessoa)

    def __str__(self):
        return "Pessoa "+str(self.id_pessoa)

    def trabalhar(self):
        sleep(5)
        self.depositar(50)

    def depositar(self, valor):
        Banco().depositar(self.id_pessoa, valor)

    def sacar(self, valor):
        Banco().sacar(self.id_pessoa, valor)

    def transferir(self, valor):
        pessoa_d = choice([pessoa for pessoa in Pessoa.lista_pessoas if pessoa != self])

        assert isinstance(pessoa_d, Pessoa)
        Banco().transferir(self.id_pessoa, pessoa_d.id_pessoa, valor)
