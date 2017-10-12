A corretude do projeto é garantido pelas seguintes características:

1. _**Caixa**_
   1. Cada caixa garante que apenas uma pessoa o estará utilizando por vez, através da fila thread-safe \(Queue do python\);
   2. Mesmo que sejam criadas duas operações de transferência gerando uma dependência, por causa da fila thread-safe dos caixas, uma dessas operações será realizada antes;
2. _**Conta**_
   1. Cada conta garante que apenas uma operação esteja sendo executada sobre ela, através do Reentrant Lock;
3. _**Banco**_
   1. O banco bloqueia a execução de toda e qualquer operação \(através da flag do Event object\) antes de adquirir o lock de todas as contas, eliminando dependência circular entre o investimento e alguma operação de transferência \(que adquiri o lock de duas contas\);
4. _**Operações**_
   1. Cada operação verifica a situação da conta após a execução, e se o estado da conta não corresponde com o esperado é feito o roll back da operação \(anulando toda e qualquer alteração sobre as contas envolvidas na operação\). Garantindo a consistência dos valores das contas.



