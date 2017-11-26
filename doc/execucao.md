# Servidores

```py
if __name__ == "__main__":
    Banco()
    StartNameServer("l_env/bin/activate")
    sleep(3)

    SocketServer().start()
    RMIServer().start()
    StartRestServer()
```

# Clientes

```py
for _ in range(0, 1):
    PessoaRMI() # Pessoa 1
    PessoaSocket() # Pessoa 2
    PessoaRest() # Pessoa 3

    DependenteRMI() # Pessoa 4
    DependenteSocket() # Pessoa 5
    DependenteRest() # Pessoa 6

Pessoa.start()
```



