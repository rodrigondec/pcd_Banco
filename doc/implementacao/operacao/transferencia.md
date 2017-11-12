# Transferência

## Descrição

A transferência é realizado em cima de duas contas. Ao iniciar a execução, a operação irá adquirir os lock das contas e os liberará ao terminar de fazer o processamento e verificação de consistência.

A operação transferência utiliza as operações de saque e depósito para realizar o processamento.

> OBS.: O lock da conta será adquirido três vezes ao realizar o execute\(\) da operação. Desta forma garantindo que a operação { saque\(saldo+saque\) + depósito\(saldo+depósito\) } ocorra atomicamente

## Código

```py
class Transferencia(OperacaoBinary):
    """Operação de transferência"""
    def __init__(self, pessoa_o, valor, pessoa_d):
        OperacaoBinary.__init__(self, pessoa_o, pessoa_d)
        self.valor = valor
        self.conta_o = None
        self.conta_d = None
        self.op_saque_o = None
        self.op_deposito_d = None

    def execute(self):
        if not self.call_before:
            return False
        try:
            self.conta_o.lock.acquire()
            self.conta_d.lock.acquire()

            self.op_saque_o = Saque(self.pessoa, self.valor)
            self.op_saque_o.before(self.conta_o)
            self.op_saque_o.execute()

            self.op_deposito_d = Deposito(self.pessoa_d, self.valor)
            self.op_deposito_d.before(self.conta_d)
            self.op_deposito_d.execute()

            self.after()
        except (SaqueException, DepositoException):
            self.roll_back()
            raise TransfException()
        finally:
            self.conta_o.lock.release()
            self.conta_d.lock.release()

    def after(self):
        pass

    def roll_back(self):
        self.op_saque_o.roll_back()
        self.op_deposito_d.roll_back()
```