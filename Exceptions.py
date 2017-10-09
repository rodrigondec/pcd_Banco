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
