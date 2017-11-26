# Instruções

## Requerimentos

* [Python 3.6.3](https://www.python.org/downloads/release/python-363/)
* [Pyro4](https://pythonhosted.org/Pyro4/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Restplus](https://flask-restplus.readthedocs.io/en/stable/)

### Preparando o ambiente virtual

* Crie o ambiente virtual via console usando `python -m venv env` 
* Ative o ambiente virtual \(e você irá precisar refazer este único passo sempre que executar usar o sistema\):

  * No Windows, execute no prompt \(cmd\): `env\Scripts\activate.bat`

  * No Unix ou MacOS, execute no terminal \(bash\): `source env/bin/activate`

* Rode o `pip` para instalar as dependências do sistema com `pip install -r requirements.txt`.

## Executando

Para executar o programa, deverá ser rodado os comandos abaixo dentro da pasta raiz do projeto.

Durante a execução dos programas, são salvos arquivos `<nome>.log` na pasta `/logs` do programa contendo as informações fornecidas durante a execução.

### Servidor

```
python server.py
```

### Clientes

```
python clients.py
```



