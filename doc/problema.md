# Problema

## Descrição

Um banco possui várias contas, cada uma pertencente a uma pessoa ou a um responsável de uma pessoa.

Ele deverá gerenciar o acesso ao recurso compartilhado dinheiro das diversas contas entre as pessoas, garantindo a concistência do valor em um cenário em que há concorrência, mediante as diversas formas de operação \(deposito, saque, saldo e trasnferência\).

Além disso, é do interesse do banco utilizar o dinheiro dos seus clientes para investir, bloqueando o acesso à ele.

Para que as pessoas realizem operações no banco, é disponibilizado 3 servidores com 3 diferentes tipos de acesso. Com eles recebendo requisições via _**Socket**_, _**RMI**_ e _**Rest**_.

## Entidades

* Conta
* Banco
* Operação Bancária
* Pessoa
* Dependente



