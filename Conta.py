from threading import RLock

class Conta(object):
    """Conta"""

    def __init__(self, id_pessoa):
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
            raise Exception('Saldo Insuficiente!')
        return True

    def sacar(self, valor):
        with self.lock:
            self._verificar_saldo_suf(valor)
            self.dinheiro -= valor
            return True

    def depositar(self, valor):
        with self.lock:
            self.dinheiro += valor
