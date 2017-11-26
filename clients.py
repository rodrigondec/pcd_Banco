from dominio.Pessoa import Pessoa, PessoaSocket, DependenteSocket, PessoaRMI, DependenteRMI, PessoaRest, DependenteRest

for _ in range(0, 1):
    PessoaRMI() # Pessoa 1
    PessoaSocket() # Pessoa 2
    PessoaRest() # Pessoa 3

    DependenteRMI() # Pessoa 4
    DependenteSocket() # Pessoa 5
    DependenteRest() # Pessoa 6

Pessoa.start()
