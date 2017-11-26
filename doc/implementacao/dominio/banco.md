# Banco

## Descrição

A classe Banco interage diretamente com a classe Conta, utilizando seus métodos de acesso para os objetos já instânciados. O Banco utiliza o pattern Singleton, garantindo que só haverá uma instância do objeto durante a execução do código.

O Banco possui uma thread que de tempos em tempos irá investir o dinheiro dos clientes, e durante o investimento bloqueará a execução de operações.

A sincronização da espera do investimento foi feita através do [Event object](https://docs.python.org/3/library/threading.html#event-objects) do Python 3. Quando o investimento terminar, todas as requisições de operações feitas pelas pessoas irão prosseguir com a execução.

## Diagrama

![](/doc/img/banco.png)

## Código

```py
from threading import Thread, Event
from time import sleep
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
        sleep(20)
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

    def realizar_operacao(self, operacao):
        if operacao.get_id_pessoa() not in Conta.contas:
           self.criar_conta(operacao.get_id_pessoa())
        if not self.disponivel.is_set():
            Banco.log.info("Pessoa {} espera banco terminar de investir".format(operacao.id_pessoa))
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
```



