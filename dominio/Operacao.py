from dominio.Exceptions import DepositoException, SaqueException, TransfException


class Operacao(object):
    """Operação bancária"""
    def __init__(self, id_pessoa):
        if self.__class__ is Operacao:
            raise TypeError('abstract class cannot be instantiated')
        self.id_pessoa = id_pessoa
        self.call_before = False

    def execute(self):
        raise NotImplementedError

    def after(self):
        raise NotImplementedError

    def roll_back(self):
        raise NotImplementedError

    def get_id_pessoa(self):
        return self.id_pessoa

    def __str__(self):
        return "{} pessoa {}".format(type(self), self.id_pessoa)

    def toJson(self):
        return {'classe': type(self).__name__, 'objeto': self.__dict__}


class OperacaoUnary(Operacao):
    """Operaçções envolvendo apenas uma id_pessoa"""
    def __init__(self, id_pessoa):
        if self.__class__ is OperacaoUnary:
            raise TypeError('abstract class cannot be instantiated')
        Operacao.__init__(self, id_pessoa)
        self.conta = None

    def before(self, conta):
        self.conta = conta
        self.call_before = True


class OperacaoBinary(Operacao):
    """Operações envolvendo duas id_pessoas"""
    def __init__(self, id_pessoa_o, id_pessoa_d):
        if self.__class__ is OperacaoBinary:
            raise TypeError('abstract class cannot be instantiated')
        Operacao.__init__(self, id_pessoa_o)
        self.id_pessoa_d = id_pessoa_d

    def before(self, conta_o, conta_d):
        self.conta_o = conta_o
        self.conta_d = conta_d
        self.call_before = True

    def get_id_pessoa_d(self):
        return self.id_pessoa_d


class Saldo(OperacaoUnary):
    """Operação de saldo"""
    def __init__(self, id_pessoa):
        OperacaoUnary.__init__(self, id_pessoa)
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
    def __init__(self, id_pessoa, valor):
        OperacaoUnary.__init__(self, id_pessoa)
        self.valor = valor
        self.conta = None
        self.valor_original = None

    def execute(self):
        if not self.call_before:
            return False

        saldo = None

        try:
            self.conta.lock.acquire()

            op_saldo = Saldo(self.id_pessoa)
            op_saldo.before(self.conta)
            self.valor_original = op_saldo.execute()

            self.conta.depositar(self.valor)

            saldo = self.after()
        finally:
            self.conta.lock.release()

        return saldo

    def after(self):
        saldo = self.conta.saldo()
        if saldo != (self.valor_original+self.valor):
            self.roll_back()
            raise DepositoException()
        return saldo

    def roll_back(self):
        self.conta.dinheiro = self.valor_original


class Saque(OperacaoUnary):
    """Operação de saque"""
    def __init__(self, id_pessoa, valor):
        OperacaoUnary.__init__(self, id_pessoa)
        self.valor = valor
        self.conta = None
        self.valor_original = None

    def execute(self):
        if not self.call_before:
            return False
        try:
            self.conta.lock.acquire()

            op_saldo = Saldo(self.id_pessoa)
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
    def __init__(self, id_pessoa_o, valor, id_pessoa_d):
        OperacaoBinary.__init__(self, id_pessoa_o, id_pessoa_d)
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

            self.op_saque_o = Saque(self.id_pessoa, self.valor)
            self.op_saque_o.before(self.conta_o)
            self.op_saque_o.execute()

            self.op_deposito_d = Deposito(self.id_pessoa_d, self.valor)
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
