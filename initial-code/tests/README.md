# Bateria de testes para o projeto TupleSpaces - SD 2025

## Antes de começar

Cada teste corresponde a um ficheiro `input*.txt` cujo conteúdo é uma sequência de comandos que o cliente deve executar.
Para cada ficheiro `input*.txt`, existe um ficheiro `expected/out*.txt` com o *output* que se espera observar na consola do cliente.

Uma bateria de testes começa pelo `input01.txt` e avança pelos testes com índices consecutivos (`input01.txt`, `input02.txt`, `input03.txt`, ...). 
A bateria termina assim que o teste do próximo índice não existir.

O *shell script* que executa a bateria de testes assume o cliente Java apenas. 
Se quiserem testar o cliente Python, podem modificar a linha do *script* em que o cliente é executado.


## Como usar?

1. Editar *shell script* `run_tests.sh` e confirmar que as variáveis na secção *PATHS* estão de acordo com a estrutura do seu projeto.

2. Compilar todas as componentes do projeto.

3. Lançar o(s) servidor(es) e o *front-end*.

3. Finalmente, executar `run_tests.sh`. Este *script* lançará o cliente Java, assumindo que o *goal* `exec:java` (configurado no `pom.xml` do cliente) já passa os argumentos de linha de comando necessários.

4. Observar quais testes falharam. Para esses, consultar os ficheiros na diretoria `tests-output` 
(que contêm os *outputs* gerados em cada teste) e compará-los com os ficheiros respetivos na diretoria `expected`.


## Perguntas frequentes

- *Podemos inventar novos testes e adicioná-los à bateria?* 
Sim, recomendamos que o façam! 
A bateria de testes que fornecemos é intencionalmente curta. Devem estendê-la com outros testes que achem relevantes.

- *Os servidores/*front-end* são terminados e lançados de novo a cada teste?* Não. Os testes assumem que os servidores/*front-end* se mantêm em execução durante a bateria inteira de testes. Logo, é necessário que cada teste não deixe marcas no estado dos servidores. Por exemplo, um teste que adicione alguns tuplos deve remover esses mesmos tuplos antes de terminar.

- *O nosso projeto será avaliado exclusivamente com testes automáticos como estes?* 
Não. A avaliação do código dos projetos não é automática. 
No entanto, usaremos alguns testes como aqueles que aqui fornecemos para 
*guiar* a análise manual que os docentes farão do código submetido por cada grupo.
