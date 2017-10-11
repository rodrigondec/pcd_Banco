# Descrição

A classe caixa possui a persistência do dicionário \(hash-map\) de contas. Cada conta está associada à um `id_pessoa` do objeto [Pessoa](/doc/implementacao/pessoa.md) e possui um [Reentrant Lock object](https://docs.python.org/3/library/threading.html#threading.RLock) do Python 3. 

Todo método irá adquirir o lock e liberá-lo após o processamento do método, fazendo assim a exclusão mútua sobre cada conta individualmente.

# Diagrama

![](/doc/img/conta.png)

# Código

```
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
    def get_conta(id_pessoa):
        assert isinstance(id_pessoa, str)
        return Conta.contas[id_pessoa]
```



