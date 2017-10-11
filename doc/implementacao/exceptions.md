# Descrição

Implementação das exceções lançadas e tratadas pelo sistema do banco, representando a falha na realização de alguma operação.

# Diagrama

![](/doc/img/exceptions.png)

# Código

```
class TransfException(Exception):
    """Exception de transferência"""
    def __init__(self, message="Erro na transferencia"):
        self.message = message

    def __str__(self):
        return repr(self.message)


class SaldoException(Exception):
    """Exception de saldo"""
    def __init__(self, message="Saldo insuficiente"):
        self.message = message

    def __str__(self):
        return repr(self.message)


class DepositoException(Exception):
    """Exception de saldo"""
    def __init__(self, message="Erro no deposito!"):
        self.message = message

    def __str__(self):
        return repr(self.message)


class SaqueException(Exception):
    """Exception de saldo"""
    def __init__(self, message="Erro no saque!"):
        self.message = message

    def __str__(self):
        return repr(self.message)

```



