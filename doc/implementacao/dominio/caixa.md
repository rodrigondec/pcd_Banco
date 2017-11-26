# Caixa

## Descrição

A classe Caixa possui a persistência da lista de caixas e a fila \([Queue object](https://docs.python.org/3/library/queue.html#queue-objects) do python 3\) compartilhada. Cada caixa possui sua própria thread que irá ficar chamando o próximo da fila \(que é thread-safe\).

A sincronização da espera da utilização do caixa pela pessoa foi feita através do [Event object](https://docs.python.org/3/library/threading.html#event-objects) do Python 3. Quando a pessoa terminar a utilização, ela altera a flag do objeto, e a execução do caixa prossegue.

## Diagrama

![](/doc/img/caixa.png)

## Código

```py
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
```