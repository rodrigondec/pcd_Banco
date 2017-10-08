from threading import Thread, Lock
from Logger import Log
from queue import Queue


class Caixa(object):
    """Caixa bancário"""

    log = Log("caixa")
    id_caixa = 0
    fila = Queue()

    def __init__(self):
        Caixa.id_caixa += 1
        self.id_caixa = str(Caixa.id_caixa)
        self.lock = Lock()
        self.thread = Thread(target=self.run, name=('Caixa ' + self.id_caixa))

    def __str__(self):
        return self.id_caixa

    def run(self):
        while True:
            Caixa.log.info("espera fila")
            pessoa = Caixa.fila.get()
            Caixa.log.info(pessoa + " está usando o caixa")
            pessoa.vez.set()
            Caixa.log.info("espera " + pessoa + " terminar de usar")
            if not pessoa.uso_caixa.is_set():
                pessoa.uso_caixa.wait()
