from dominio.Pessoa import Pessoa, PessoaSocket, DependenteSocket, PessoaRMI, DependenteRMI, PessoaRest, DependenteRest

for _ in range(0, 1):
    PessoaRMI() # Pessoa 1
    PessoaSocket() # Pessoa 2

    DependenteRMI() # Pessoa 3
    DependenteSocket() # Pessoa 4

    PessoaRest() # Pessoa 5
    DependenteRest() # Pessoa 6

Pessoa.start()