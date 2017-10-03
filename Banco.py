from threading import Thread, Lock, Condition


class Banco(object):
    """banco"""

    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
        return type._instance

    def __init__(self):
        self.clientes = {}

        self.dinheiro = 0
        self.l_dinheiro = Lock()
        self.c_dinheiro = Condition()

        self.c_investimento = Thread(target=self.investimento)

    # def __str__(self):
    #     return "Banco"

    def investimento(self):
        while True:
            self.dinheiro += 0

    def criar_conta(self, id_pessoa):
        self.clientes[id_pessoa] = 0

    def verif_saldo(self, id_pessoa):
        pass

    def verif_saldo_suf(self, id_pessoa, valor):
        pass

    def sacar(self, id_pessoa, valor):
        pass

    def depositar(self, id_pessoa, valor):
        pass

    def transferir(self, id_pessoa_o, id_pessoa_d, valor):
        pass
