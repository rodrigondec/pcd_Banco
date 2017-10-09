from threading import RLock
from Exceptions import SaldoException

class Conta(object):
    """Conta"""

    contas = {}

    def __init__(self, id_pessoa):
        assert isinstance(id_pessoa, str)

        Conta.contas[id_pessoa] = self
        self.id_pessoa = id_pessoa
        self.dinheiro = 0
        self.lock = RLock()

    def __str__(self):
        return "Conta da pessoa "+str(self.id_pessoa)

    def saldo(self):
        with self.lock:
            return self.dinheiro

    def _verificar_saldo_suf(self, valor):
        if self.saldo() < valor:
            raise SaldoException("tem na conta {saldo}. faltam {saque} para sacar {valor}".format(saldo=self.saldo(), saque=valor-self.saldo(), valor=valor))

    def sacar(self, valor):
        with self.lock:
            self._verificar_saldo_suf(valor)
            self.dinheiro -= valor

    def depositar(self, valor):
        with self.lock:
            self.dinheiro += valor
        return

    @staticmethod
    def realizar_saque(id_pessoa, valor):
        assert isinstance(id_pessoa, str)
        Conta.contas[id_pessoa].sacar(valor)

    @staticmethod
    def realizar_deposito(id_pessoa, valor):
        assert isinstance(id_pessoa, str)
        Conta.contas[id_pessoa].depositar(valor)

    @staticmethod
    def ver_saldo(id_pessoa):
        assert isinstance(id_pessoa, str)
        return Conta.contas[id_pessoa].saldo()

    @staticmethod
    def get_conta(id_pessoa):
        assert isinstance(id_pessoa, str)
        return Conta.contas[id_pessoa]
