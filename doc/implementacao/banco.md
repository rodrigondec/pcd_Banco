<<<<<<< Updated upstream
# Banco

## Descrição

A classe Banco interage diretamente com as classes Caixa e Conta, utilizando seus métodos de acesso para os objetos já instânciados. O Banco utiliza o pattern Singleton, garantindo que só haverá uma instância do objeto durante a execução do código.

O Banco possui uma thread que de tempos em tempos irá investir o dinheiro dos clientes, e durante o investimento bloqueará a execução de operações.

A sincronização da espera do investimento foi feita através do [Event object](https://docs.python.org/3/library/threading.html#event-objects) do Python 3. Quando o investimento terminar, todas as requisições de operações feitas pelas pessoas irão prosseguir com a execução.

Toda operação recebida pelo banco é adicionada na fila dos caixas, na qual esperarão sua vez de serem processadas de acordo com a classe Caixa.

## Diagrama

![](/doc/img/banco.png)

## Código

```py
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
```



=======
# Descrição

A classe Banco interage diretamente com as classes Caixa e Conta, utilizando seus métodos de acesso para os objetos já instânciados. O Banco utiliza o pattern Singleton, garantindo que só haverá uma instância do objeto durante a execução do código.

O Banco possui uma thread que de tempos em tempos irá investir o dinheiro dos clientes, e durante o investimento bloqueará a execução de operações.

A sincronização da espera do investimento foi feita através do [Event object](https://docs.python.org/3/library/threading.html#event-objects) do Python 3. Quando o investimento terminar, todas as requisições de operações feitas pelas pessoas irão prosseguir com a execução.

Toda operação recebida pelo banco é adicionada na fila dos caixas, na qual esperarão sua vez de serem processadas de acordo com a classe Caixa.

# Diagrama

![](/doc/img/banco.png)

# Código

```py
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
```



>>>>>>> Stashed changes
