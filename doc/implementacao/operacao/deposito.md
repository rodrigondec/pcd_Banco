# Descrição

O depósito é realizado em cima de uma conta. Ao iniciar a execução, a operação irá adquirir o lock da conta e o liberará ao terminar de fazer o processamento e verificação de consistência.

A operação depósito utiliza a operação saldo para realizar a vefiricação de consistência.

> OBS.: O lock da conta será adquirido duas vezes ao realizar o execute\(\) da operação. Desta forma garantindo que a operação \(saldo+depósito\) ocorra atomicamente

# Código

```py
class Deposito(OperacaoUnary):
    """Operação de depósito"""
    def __init__(self, pessoa, valor):
        OperacaoUnary.__init__(self, pessoa)
        self.valor = valor
        self.conta = None
        self.valor_original = None

    def execute(self):
        if not self.call_before:
            return False
        try:
            self.conta.lock.acquire()

            op_saldo = Saldo(self.pessoa)
            op_saldo.before(self.conta)
            self.valor_original = op_saldo.execute()

            self.conta.depositar(self.valor)

            self.after()
        finally:
            self.conta.lock.release()

    def after(self):
        if self.conta.saldo() != (self.valor_original+self.valor):
            self.roll_back()
            raise DepositoException()
        return True

    def roll_back(self):
        self.conta.dinheiro = self.valor_original
```



