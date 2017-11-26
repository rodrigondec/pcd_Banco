# Dependente

## Descrição

O Dependente é uma generalização da classe Pessoa. Alterando apenas o retorno do id vinculado à conta \(que será o do responsável\) e o método para pegar a listagem de pessoas disponíveis para transferência.

## Código

```py
class Dependente(Pessoa):
    """Pessoa dependente"""

    def __init__(self):
        self.responsavel = choice([pessoa for pessoa in Pessoa.lista_pessoas if not isinstance(pessoa, Dependente)])
        Pessoa.__init__(self)
        print(self)

    def __str__(self):
        return "Pessoa {}, dependente de {}".format(self.id_pessoa, self.responsavel.id_pessoa)

    def _get_lista_pessoa(self):
        return [pessoa for pessoa in Pessoa.lista_pessoas if not isinstance(pessoa, Dependente) and pessoa != self.responsavel]

    def get_id(self):
        return self.responsavel.id_pessoa
```