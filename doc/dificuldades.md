# Consistência

Uma das dificuldades encontradas durante a implementação do projeto foi como modelar as operações bancárias de uma forma que elas sejam atômicas e garantam a consistência das contas após a execução \(caso tenha ocorrido algum erro durante a execução\).

## Atomicidade

No início da implementação era utiliza um Lock normal, e não um Reentrant Lock. 

E por causa disso não havia a atomicidade em operações compostas, como por exemplo a de depósito que iniciava uma operação de saldo sobre a conta para depois realizar o depósito em si. 

A operação iniciava, verificada o saldo \(adquirindo e liberando o lock da conta ao terminar de ver o saldo\) e depois executava o deposito \(adquirindo e liberando o lock da conta ao terminar de depositar\) e na janela de tempo entre ver o saldo e depositar outra operação poderia adquirir o lock da conta e alterar o valor. E por causa dessa operação intrusa, a consistência da operação realizada não era garantida.

Ao utilizar o Reentrant Lock, cada operação adquiri novamente os locks das contas involvidas antes de realizar as sub-operações dentro dela. Garantindo assim a atomicidade.

# Deadlock

Outra dificuldade foi com relação à deadlock, no qual ocorria se as seguintes condições ocorressem:

1. O banco inicia a operação de investimento, e começa a adquirir os locks de todas as contas;
2. Havia uma operação de trasnferência ocorrendo ao mesmo tempo, que conseguiu pegar o primeiro lock mas o segundo lock já foi adquirido pelo banco ao iniciar o investimento.

Dessa forma, gerando uma dependência circular sobre os locks das contas. Isso ocorria apenas com a operação de transferência, dificultando a percepção desse erro.



