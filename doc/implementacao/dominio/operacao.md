# Operação

## Descrição

As operações bancárias foram implementadas seguindo o pattern command.

## Diagrama![](/doc/img/operacao.png)

## Código Template

```py
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
```



