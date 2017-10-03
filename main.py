from Banco import Banco
from Pessoa import Pessoa


qt_pessoas = 15

Banco()

for _ in range(0, qt_pessoas):
    Pessoa()

banco1 = Banco()
banco2 = Banco()
print(banco1, banco2)
