from threading import Thread, Event
from time import sleep
import Pyro4
from dominio.Operacao import Operacao, OperacaoUnary, OperacaoBinary
from dominio.Conta import Conta
from dominio.Logger import Log


class Banco(object):
    """banco"""
    log = Log("banco")

    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance.init()
        return type._instance

    def init(self):
        self.disponivel = Event()
        self.disponivel.set()

        self.thread = Thread(target=self.investimento, name='Banco_Investimento')
        self.thread.start()

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

    def criar_conta(self, id_pessoa):
        Conta(id_pessoa)

    @Pyro4.expose
    def realizar_operacao(self, operacao):
        if operacao.get_id_pessoa() not in Conta.contas:
           self.criar_conta(operacao.get_id_pessoa())
        if not self.disponivel.is_set():
            # type(operacao.pessoa).log.info("espera banco terminar de investir")
            self.disponivel.wait()

        assert isinstance(operacao, Operacao)
        if isinstance(operacao, OperacaoUnary):
            operacao.before(Conta.get_conta(operacao.get_id_pessoa()))
        elif isinstance(operacao, OperacaoBinary):
            if operacao.get_id_pessoa_d() not in Conta.contas:
                self.criar_conta(operacao.get_id_pessoa_d())
            operacao.before(conta_o=Conta.get_conta(operacao.get_id_pessoa()),
                            conta_d=Conta.get_conta(operacao.get_id_pessoa_d()))

        return operacao.execute()
