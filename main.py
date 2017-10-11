from Banco import Banco
from Pessoa import Pessoa, Dependente
from time import sleep

qt_pessoas = 2
qt_dependentes = 3
Banco.qt_caixas = 2

Banco()

for _ in range(0, qt_pessoas):
    Pessoa()

for _ in range(0, qt_dependentes):
    Dependente()
    # sleep(3)

Pessoa.start()
