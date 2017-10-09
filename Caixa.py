from threading import Thread
from Logger import Log
from queue import Queue


class Caixa(object):
    """Caixa bancário"""

    log = Log("caixa")
    id_caixa = 0
    caixas = []
    fila = Queue()

    def __init__(self):
        Caixa.id_caixa += 1
        Caixa.caixas.append(self)
        self.id_caixa = str(Caixa.id_caixa)

        self.thread = Thread(target=self.run, name=('Caixa ' + self.id_caixa))
        self.thread.start()

    def __str__(self):
        return self.id_caixa

    def run(self):
        while True:
            pessoa = Caixa.fila.get()

            Caixa.log.info("{} esta usando o caixa".format(pessoa))
            pessoa.vez.set()

            if not pessoa.uso_caixa.is_set():
                Caixa.log.info("espera {} terminar de usar".format(pessoa))
                pessoa.uso_caixa.wait()
