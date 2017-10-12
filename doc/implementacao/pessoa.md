# Pessoa

## Descrição

A classe Pessoa possui a persistência do dicionário \(hash-map\) de pessoas. Cada pessoa possui sua própria thread que irá controlar a vida da pessoa. A pessoa realiza uma ação randômica entre trabalhar, gastar e transferir; e após isso dorme por 5 segundos.

A ação de trabalhar envolve dormir por 5 segundos e depois depositar o dinheiro que a pessoa possui.

A ação gastar envolve escolher uma quantia aleatória entre 10 e 300, e se a pessoa não tiver dinheiro vivo com ela \(cada pessoa possui sua própria carteira de dinheiro além do banco\) tentar sacar o que falta para a quantia desejada.

A ação transferir envolve escolher envolve escolher uma quantia aleatória entre 50 e 200 e uma pessoa \(que não seja ela mesma e nem um dependente\), e de fato transferir a quantia para a pessoa em questão.

Cada operação \(saque, saldo, depósito ou transferência\) irá invocar o método de realizar operação do Banco e irá travar ou não a thread da pessoa de acordo com as sincronizações das classes Banco, Operação, Caixa e Conta.

Como toda ação irá se tornar uma Operação, que por sua vez irá ser adicionada à fila de caixas, a pessoa possui dois atributos de sincronização que são do tipo [Event object](https://docs.python.org/3/library/threading.html#event-objects) do Python 3. Sendo eles:

* _**Pessoa.vez**_ representando a vez de utilização do caixa referente à fila da classe Caixa;
* E _**Pessoa.uso\_caixa**_ representando que a pessoa terminou de utilizar o caixa, sinalizando para o caixa que o estava esperando continuar com sua execução.

## Diagrama

![](/doc/img/pessoa.png)

## Código

```py
class Pessoa(object):
    """pessoa"""
    count_pessoas = 0
    lista_pessoas = []
    log = Log('pessoa')

    @staticmethod
    def start():
        for pessoa in Pessoa.lista_pessoas:
            pessoa.thread.start()

    def __init__(self):
        Pessoa.count_pessoas += 1
        self.id_pessoa = str(Pessoa.count_pessoas)
        Pessoa.lista_pessoas.append(self)
        Banco().criar_conta(self)

        self.dinheiro = 0
        self.triste = False

        self.vez = Event()
        self.vez.clear()

        self.uso_caixa = Event()
        self.uso_caixa.clear()

        self.thread = Thread(target=self.viver, name=self)

    def __str__(self):
        return "Pessoa "+self.id_pessoa

    def viver(self):
        while True:
            self.uso_caixa.clear()
            self.vez.clear()
            self.fazer_acao()
            sleep(5)

    def fazer_acao(self):
        acao = randrange(1, 4)
        if self.triste:
            acao = 2
        if acao == 1:
            self.gastar(randrange(10, 300, 10))
        elif acao == 2:
            self.trabalhar(randrange(10, 70, 10))
        elif acao == 3:
            self.transferir(randrange(50, 200, 50))
        self.uso_caixa.set()

    def trabalhar(self, valor):
        Pessoa.log.info("vai trabalhar")
        sleep(5)
        Pessoa.log.info("ganhou "+str(valor))
        self.dinheiro += valor
        self.depositar()

    def gastar(self, valor):
        Pessoa.log.info("vai gastar " + str(valor))
        try:
            if self.dinheiro < valor:
                Pessoa.log.info("nao tem dinheiro vivo o suficiente. falta {}".format(valor-self.dinheiro))
                self.sacar(valor-self.dinheiro)
            self.dinheiro = 0
            Pessoa.log.info("gastou {}".format(valor))
        except SaldoException as e:
            Pessoa.log.info("{}. Ela esta triste :c".format(e.message))
            self.triste = True

    def depositar(self):
        Pessoa.log.info("vai depositar {}".format(self.dinheiro))
        quantia = self.dinheiro
        Banco().realizar_operacao(operacao=Deposito(self, quantia))
        self.dinheiro = 0
        Pessoa.log.info("depositou {}. Ela tem agora {} no banco."
                        " Ela esta satisfeita".format(quantia, Banco().realizar_operacao(operacao=Saldo(self))))
        self.triste = False

    def sacar(self, valor):
        Pessoa.log.info("vai sacar "+str(valor))
        Banco().realizar_operacao(Saque(self, valor))
        Pessoa.log.info("sacou {}. Ela esta feliz :D".format(valor))

    def _get_lista_pessoa(self):
        return [pessoa for pessoa in Pessoa.lista_pessoas if pessoa != self and not isinstance(pessoa, Dependente)]

    def transferir(self, valor):
        pessoa_d = choice(self._get_lista_pessoa())
        Pessoa.log.info("vai transferir {} para Pessoa {}".format(valor, pessoa_d))

        assert isinstance(pessoa_d, Pessoa)
        try:
            Banco().realizar_operacao(Transferencia(self, valor, pessoa_d))
            Pessoa.log.info("transferiu {} para Pessoa {}".format(valor, pessoa_d))
        except (SaldoException, TransfException) as e:
            Pessoa.log.info("{}. Ela esta triste :c".format(e.message))
            self.triste = True

    def get_id(self):
        return self.id_pessoa
```



