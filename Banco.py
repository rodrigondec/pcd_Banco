from threading import Thread, RLock, Condition, Event
from Logger import Log
from time import sleep


class Banco(object):
    """banco"""
    log = Log("banco")

    def __new__(type):
        if not '_instance' in type.__dict__:
            type._instance = object.__new__(type)
            type._instance.init()
        return type._instance

    def init(self):
        self.clientes = {}
        self.clientes_investimento = {}

        self.dinheiro = 0
        self.l_dinheiro = RLock()

        self.dinheiro_investimento = Event()
        self.dinheiro_investimento.clear()

        self.operacao_liberada = Event()
        self.operacao_liberada.set()

        self.t = Thread(target=self.investimento)
        self.t.start()

        self.t_consistencia = Thread(target=self.confirir_consistencia)
        self.t_consistencia.start()

    def __str__(self):
        return "Banco"

    def confirir_consistencia(self):
        while True:
            quantia = 0
            for id_pessoa, valor in self.clientes.items():
                quantia += valor
            if quantia != self.dinheiro:
                Banco.log.print("Banco ERRO NO DINHEIRO!!!!!!!!!!!!!!!!!!!!!!!!!"
                                "\n\tClientes tem "+str(quantia)+" mas o banco so tem "+str(self.dinheiro))
            else:
                Banco.log.print("Banco OK! Ele tem "+str(self.dinheiro))
            sleep(1)


    def investimento(self):
        while True:
            Banco.log.print("Banco pergunta, tenho dinheiro pra investir?")
            if not self.dinheiro_investimento.is_set():
                Banco.log.print("Banco esperando condicao para investir")
                Banco().dinheiro_investimento.wait()
            with self.l_dinheiro:

                Banco.log.print("Banco investindo o dinheiro dos clientes. Bloqueando operacoes de saque e "
                                "transferencia")
                self.operacao_liberada.clear()

                self.dinheiro = 0
                for id_pessoa, valor in self.clientes.items():
                    self.clientes[id_pessoa] = 0
                    self.clientes_investimento[id_pessoa] = valor

                sleep(8)

                for id_pessoa, valor in self.clientes_investimento.items():
                    self.dinheiro += valor + valor / 10
                    self.clientes[id_pessoa] += valor + valor / 10
                    self.clientes_investimento[id_pessoa] = 0

                Banco.log.print("Banco terminou de investir")
                self.operacao_liberada.set()

            sleep(15)

    def criar_conta(self, id_pessoa):
        self.clientes[str(id_pessoa)] = 0
        self.clientes_investimento[id_pessoa] = 0

    def saldo(self, id_pessoa):
        return self.clientes[id_pessoa]

    def verif_saldo_suf(self, id_pessoa, valor):
        if self.saldo(id_pessoa) < valor:
            raise Exception('Saldo Insuficiente!')
        return True

    def sacar(self, id_pessoa, valor):
        self.verif_saldo_suf(id_pessoa, valor)
        with self.l_dinheiro:
            self.clientes[id_pessoa] -= valor
            self.dinheiro -= valor
            Banco.log.print("Banco deu " + str(valor) + " para a Pessoa " + str(id_pessoa) + ". Ele tem agora " + str(
                self.dinheiro))
            if self.dinheiro < 100:
                self.dinheiro_investimento.clear()
        return valor

    def depositar(self, id_pessoa, valor):
        with self.l_dinheiro:
            self.clientes[id_pessoa] += valor
            self.dinheiro += valor
            Banco.log.print("Banco recebeu "+str(valor)+" da Pessoa "+str(id_pessoa)+". Ele tem agora "+str(self.dinheiro))
            if self.dinheiro >= 100:
                self.dinheiro_investimento.set()
        return True

    def transferir(self, id_pessoa_o, id_pessoa_d, valor):
        self.verif_saldo_suf(id_pessoa_o, valor)
        with self.l_dinheiro:
            self.sacar(id_pessoa_o, valor)
            self.depositar(id_pessoa_d, valor)
        return valor
