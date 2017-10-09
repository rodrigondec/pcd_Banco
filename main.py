from Conta import Conta
from Banco import Banco
from Pessoa import Pessoa
import logging


qt_pessoas = 4

Banco()

for _ in range(0, qt_pessoas):
    Pessoa()

Pessoa.start()
