from threading import Thread, Event
from Logger import Log
from time import sleep
from Caixa import Caixa
from Conta import Conta
from Operacao import Operacao, OperacaoUnary, OperacaoBinary


class Banco(object):
    """banco"""
    log = Log("banco")
    qt_caixas = None

    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance.init()
        return type._instance

    def init(self):
        for _ in range(0, Banco.qt_caixas):
            Caixa()

        self.disponivel = Event()
        self.disponivel.set()

        self.t = Thread(target=self.investimento, name='Banco_Investimento')
        self.t.start()

    def __str__(self):
        return "Banco"

    def investimento(self):
        sleep(10)
        while True:
            try:
                self.disponivel.clear()
                Banco.log.info("investimento iniciando")
                for id_pessoa, conta  in Conta.contas.items():
                    conta.lock.acquire()

                sleep(5)

                for id_pessoa, conta in Conta.contas.items():
                    conta.depositar(conta.saldo()/10)
                Banco.log.info("investimento terminado")
            finally:
                for id_pessoa, conta  in Conta.contas.items():
                    conta.lock.release()
                self.disponivel.set()

            sleep(15)

    def criar_conta(self, pessoa):
        Conta(pessoa.get_id())

    def realizar_operacao(self, operacao):
        if not self.disponivel.is_set():
            type(operacao.pessoa).log.info("espera banco terminar de investir")
            self.disponivel.wait()

        assert isinstance(operacao, Operacao)
        if isinstance(operacao, OperacaoUnary):
            operacao.before(Conta.get_conta(operacao.pessoa.get_id()))
        elif isinstance(operacao, OperacaoBinary):
            operacao.before(conta_o=Conta.get_conta(operacao.pessoa.get_id()),
                            conta_d=Conta.get_conta(operacao.pessoa_d.get_id()))

        self._adicionar_fila(operacao.pessoa)

        return operacao.execute()

    def _adicionar_fila(self, pessoa):
        if not pessoa.vez.is_set():
            type(pessoa).log.info("entrou na fila do banco")
            Caixa.fila.put(pessoa)
            type(pessoa).log.info("espera sua vez")
            pessoa.vez.wait()
