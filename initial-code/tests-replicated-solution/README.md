# Testes concorrentes a solução replicada do projeto

Este conjunto de testes exercita diferentes situações de concorrência entre clientes. 

Ao contrário da 1ª bateria de testes, estes testes não são avaliados automaticamente. Quem executa cada teste deve observar o comportamento de cada cliente concorrente (incluindo os instantes em que cada *output* é impresso por cada cliente) e, assim, perceber se o comportamento observado é o esperado.

## Resumo dos testes:

- test1: Testa cenário em que um cliente invoca `read` e `take` sobre tuplos que ainda não estão disponíveis, logo é obrigado a esperar.
- test2: Testa `read` e `take` invocados quando só uma das réplicas tem o tuplo alvo; o `read` deve responder imediatamente mas o `take` deve esperar até que todas as réplicas tenham o tuplo.
- test3: Testa invocações concorrentes de `take` que competem pelo mesmo tuplo. Devido aos atrasos que o teste introduz, o cliente C1 deve ser o primeiro a conseguir obter a exclusão mútua do seu *voter set*; consequentemente, o cliente C2 precisará esperar até que o C1 liberte a exclusão mútua.
- E outros que o grupo queira inventar!...

## Instruções:
- Descubra como, no seu emulador de terminal favorito, qual o comando que permite executar um programa numa nova janela no terminal [ver nota abaixo]. Por exemplo, em GNOME terminal é `gnome-terminal -x`, em `xterm` é `xterm -e`, etc.
- Deve ter os servidores e o front-end lançados previamente. 
- Para executar cada teste, lance ambos os clientes simultaneamente, cada um numa janela diferente do terminal. Assim poderá observar ambos, lado a lado. 
Exemplo:

``COMANDO_NOVA_JANELA mvn exec:java -Dexec.args="..." < test1_C1.txt & COMANDO_NOVA_JANELA mvn exec:java -Dexec.args="..." < test1_C2.txt & ``

**Nota:** Se, no seu ambiente de desenvolvimento, não puder lançar automaticamente janelas de terminal novas, pode simplesmente correr ambos os clientes no mesmo terminal

## Observação final

Lembre-se que os primeiros testes (fornecidos para a 1ª entrega) também são úteis para testar o sistema replicado. No entanto, como a resposta da operação `getTupleSpaceState` será diferente num sistema replicado, deve adaptar os ficheiros da diretoria `expected` antes de testar a solução replicada com esses testes.