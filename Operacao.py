from Exceptions import DepositoException, SaqueException, TransfException


class Operacao(object):
    """Operação bancária"""
    def __init__(self, pessoa):
        if self.__class__ is Operacao:
            raise TypeError('abstract class cannot be instantiated')
        self.pessoa = pessoa
        self.call_before = False

    def execute(self):
        raise TypeError('abstract method cannot be called')

    def after(self):
        raise TypeError('abstract method cannot be called')

    def roll_back(self):
        raise TypeError('abstract method cannot be called')

    def get_id_pessoa(self):
        return self.pessoa.get_id()


class OperacaoUnary(Operacao):
    """Operaçções envolvendo apenas uma pessoa"""
    def __init__(self, pessoa):
        if self.__class__ is OperacaoUnary:
            raise TypeError('abstract class cannot be instantiated')
        Operacao.__init__(self, pessoa)
        self.conta = None

    def before(self, conta):
        self.conta = conta
        self.call_before = True


class OperacaoBinary(Operacao):
    """Operações envolvendo duas pessoas"""
    def __init__(self, pessoa_o, pessoa_d):
        if self.__class__ is OperacaoBinary:
            raise TypeError('abstract class cannot be instantiated')
        Operacao.__init__(self, pessoa_o)
        self.pessoa_d = pessoa_d
        self.conta = None

    def before(self, conta_o, conta_d):
        self.conta_o = conta_o
        self.conta_d = conta_d
        self.call_before = True


class Saldo(OperacaoUnary):
    """Operação de saldo"""
    def __init__(self, pessoa):
        OperacaoUnary.__init__(self, pessoa)
        self.conta = None

    def execute(self):
        if not self.call_before:
            return False

        valor = self.conta.saldo()

        self.after()

        return valor

    def after(self):
        return True

    def roll_back(self):
        pass


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


class Saque(OperacaoUnary):
    """Operação de saque"""
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

            self.conta.sacar(self.valor)

            self.after()
        finally:
            self.conta.lock.release()

    def after(self):
        if self.conta.saldo() != (self.valor_original-self.valor):
            self.roll_back()
            raise SaqueException()
        return True

    def roll_back(self):
        self.conta.dinheiro = self.valor_original


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
