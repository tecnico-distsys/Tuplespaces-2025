
# TupleSpaces

Este documento descreve o projeto da cadeira de Sistemas Distribuídos 2024/2025.

*Nota prévia:* Decidimos publicar o enunciado no primeiro dia de aulas para permitir que os estudantes o
comecem a ler e possam antecipar o que acontecerá ao longo do período. 
No entanto, a resolução do projeto só deve arrancar na 2ª semana de aulas, o que coincide com as aulas laboratoriais sobre programação com *gRPC*. Por isso, o código inicial do projeto só será disponibilizado nessa altura.


## 1 Introdução


O objetivo do projeto de Sistemas Distribuídos (SD) é desenvolver o sistema **TupleSpaces**, um serviço que implementa um *espaço de tuplos* distribuído. 
O sistema será concretizado usando [gRPC](https://grpc.io/) e Java (com uma exceção, descrita mais à frente neste enunciado).

O serviço permite a um ou mais utilizadores (também designados por _workers_ na literatura) colocarem tuplos no espaço partilhado, lerem os tuplos existentes, assim como retirarem tuplos do espaço. Um tuplo é um conjunto ordenado de campos *<campo_1, campo_2, ..., campo_n>*. 
Neste projeto, um tuplo deve ser instanciado como uma cadeia de caracteres (*string*).
Por exemplo, a *string* contendo `"<vaga,sd,turno1>"`.

No espaço de tuplos podem co-existir várias instâncias idênticas.
Por exemplo, podem existir múltiplos tuplos `"<vaga,sd,turno1>"`, indicando a existência de várias vagas. 

É possível procurar, no espaço de tuplos, por um dado tuplo para ler ou retirar.
Na variante mais simples, pode-se pesquisar por um tuplo concreto. Por exemplo, `"<vaga,sd,turno1>"`.
Alternativamente, é possível usar [expressões regulares Java](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html#sum) para permitir o emparelhamento com múltiplos valores. Por exemplo, `"<vaga,sd,[^,]+>"` 
tanto emparelha com  `"<vaga,sd,turno1>"`, com  `"<vaga,sd,turno2>"`.

Mais informação sobre os espaços de tuplos distribuídos, assim como a descrição de um sistema que concretiza esta abstração pode ser encontrada na bibilografia da cadeira e no seguinte artigo:

A. Xu and B. Liskov. [A design for a fault-tolerant, distributed implementation of linda](http://www.ai.mit.edu/projects/aries/papers/programming/linda.pdf). In 1989 The Nineteenth International Symposium on Fault-Tolerant Computing. Digest of Papers(FTCS), pages 199–206.

As operações disponíveis para o utilizador são as seguintes [^1] *put*, *read*, *take* e *getTupleSpacesState*.

[^1]: Usamos a nomenclatura em Inglês da bibliografia da cadeira, mas substituímos o nome *write* por *put*, que nos parece mais claro. Note-se que o artigo original usa uma nomenclatura diferente.

* A operação *put* acrescenta um tuplo ao espaço partilhado.

* A operação *read* aceita a descrição do tuplo (possivelmente com expressão regular) e retorna *um* tuplo que emparelhe com a descrição, caso exista. Esta operação bloqueia o cliente até que exista um tuplo que satisfaça a descrição. O tuplo *não* é retirado do espaço de tuplos.

* A operação *take* aceita a descrição do tuplo (possivelmente com expressão regular) e retorna *um* tuplo que emparelhe com a descrição. Esta operação bloqueia o cliente até que exista um tuplo que satisfaça a descrição. O tuplo *é* retirado do espaço de tuplos.

* A operação *getTupleSpacesState* não recebe argumentos e retorna uma lista de todos os tuplos em cada servidor.

Os utilizadores acedem ao serviço **TupleSpaces** através de um processo cliente, que interage 
com um ou mais servidores que oferecem o serviço, através de chamadas a procedimentos remotos.

## 2 Objetivos e etapas do projecto


Neste projeto, os estudantes irão:

- Desenvolver um sistema distribuído usando uma *framework* de RPC atual (gRPC), exercitando os seus principais modelos de comunicação 
(*stubs* bloqueantes e *stubs* assíncronos).

- Replicar um serviço distribuído, usando uma arquitetura realista. 

- Entender como a concorrência é prevalente num sistema distribuído: não só a concorrência entre os processos distribuídos, como
a concorrência entre as *threads* que se executam nos servidores. 
Partindo dessa concorrência, pôr em prática algoritmos que asseguram a coerência desejada.

- Ter um contacto com artigos de investigação académica, os quais descrevem alguns dos algoritmos implementados no projeto. 
Perceber como os avanços nestes domínios científicos são descritos nestes artigos.


O projeto passa por três objetivos. Dois são obrigatórios e um é opcional.

Para concretizar cada objetivo, definimos múltiplas etapas. De seguida descrevemos cada objetivo e as etapas que o constituem.

### Objetivo A

Desenvolver uma solução em que o serviço é prestado por um único servidor (ou seja, uma arquitetura cliente-servidor simples, sem replicação de servidores), que aceita pedidos num endereço/porto bem conhecido.
Os clientes interagem com um *front-end* de replicação, que por sua vez atua como mediador com o servidor.
Tanto os clientes como o *front-end* devem usar os *blocking stubs* do gRPC.

#### Etapa A.1

Sistema implementado sem *front-end*, em que os clientes interagem diretamente com o servidor.
Dois clientes disponíveis, um implementado em Java e outro em Python.

#### Etapa A.2

Com *front-end* no caminho entre clientes e servidor.

Nota: O sistema deve suportar que existam múltiplos *front-ends* em execução, cada um servindo um sub-conjunto de clientes.
No entanto, no projeto só testaremos o caso de um *front-end*.

### Objetivo B

Desenvolver uma solução alternativa em que o serviço é replicado, **em três servidores**.
Nesta solução, o *front-end* precisará recorrer a *non-blocking stubs* do gRPC.

A interface remota (ficheiro `.proto`) dos servidores replicados não é fornecida no código base.
Cada grupo deve compor essa interface remota. Recomendamos que seja uma adaptação do `TupleSpaces.proto` fornecido pelos docentes. Serão penalizadas interfaces que divirjam desnecessariamente do `TupleSpaces.proto`.


#### Etapa B.1

Desenvolver as operações _read_ e _put_ (não suportando, para já, a operação _take_), 
seguindo o algoritmo de Xu e Liskov (citado acima).
Resumidamente, quando um cliente pretende invocar uma dessas operações, 
o *front-end* começa por enviar o pedido a todos os servidores e depois aguarda pelas 
respostas (de um servidor, no caso de _read_, ou de todos os servidores, no caso de _put_).

Para permitir depurar o funcionamento do sistema replicado, deve também ser permitido que o cliente, quando invoca uma operação replicada (*read*, *put* e, mais tarde, *take*), possa opcionalmente
especificar um atraso (em segundos) que cada réplica que recebe o pedido deve 
esperar antes de o executar.
O atraso associado a cada pedido deve ser enviado como *gRPC metdata* no pedido ao *front-end* e 
pelos pedidos que o *front-end* envia às réplicas.

#### Etapa B.2

Desenvolver também o código necessário para executar a operação _take_.
Em vez da solução proposta no algoritmo de Xu/Liskov, deve
ser desenvolvida uma solução baseada no algoritmo de exclusão mútua de Maekawa, 
descrito na bibliografia da cadeira.


Conceptualmente, o *front-end* deve implementar um pedido _take_ executando os três passos seguintes:

1. Entrar na secção crítica (segundo o algoritmo de Maekawa),
2. Assim que estiver em exclusão mútua, invocar a operação _take_ em todas as réplicas e aguardar por resposta de todas,
3. Sair da secção crítica  (segundo o algoritmo de Maekawa).



Devem ser tidas em conta as seguintes restrições:

- Em relação ao espaço de tuplos centralizado, construído na etapa anterior, a solução replicada 
deve assumir a seguinte restrição: a operação _take_ só pode receber a designação de 
um tuplo concreto (ou seja, não são aceites expressões regulares como argumento à operação _take_ replicada).

- Deve assumir-se que cada cliente tem um *client_id* numérico, que é passado como argumento quando o cliente é lançado. 
Dado esse *client_id*, o *voter set, V_i,* usado pelo algoritmo de Maekawa deve ser o seguinte: *{client_id mod 3, (client_id + 1) mod 3}* (em que cada elemento no conjunto identifica uma réplica, de 0 a 2).

- Fica de fora deste projeto prevenir situações de interblocagem (*deadlock*).

- O algoritmo descrito no artigo original de Maekawa inclui diferenças importantes que não devem 
ser consideradas neste projeto. Por outras palavras, a referência é o algoritmo descrito na bibliografia da cadeira.


Valorizaremos implementações que, embora respeitando o desenho 
descrito acima, permitam que o sistema replicado sirva em paralelo pedidos *take* a tuplos diferentes.


### Objetivo C

Refinar a solução obtida no objetivo anterior.

#### Etapa C.1

Estender a solução de forma a permitir que a operação *take* passe a poder também receber uma expressão regular 
como argumento.
Tal como na solução construída anteriormente, o primeiro passo do algoritmo continuar a enviar o
pedido a um *voter set* apenas.

#### Etapa C.2

Otimizar a solução composta na etapa B.2, tentando reduzir o número de mensagens trocadas e/ou o tempo de espera no caminho crítico do *front-end*.

Sugestão: ver a discussão na secção 4.2 do artigo de Xu e Liskov.


Para submissão da solução para as etapas C.1 e/ou C.2, além do código da solução, é também exigido que 
cada grupo submeta um documento com um máximo de 2 páginas a descrever o desenho da solução.
O formato desse documento encontra-se disponível [aqui](https://github.com/tecnico-distsys/Tuplespaces-2025/blob/master/OrientacoesRelatorioFinalSD.md).


## 3 Faseamento da execução do projeto

Os alunos poderão optar por desenvolver apenas os objetivos A e B do projecto (nível de dificuldade "Bring 'em on!") ou também o objetivo C (nível de dificuldade "I am Death incarnate!"). Note-se que o nível de dificuldade "Don't hurt me" não está disponível neste projecto.

O nível de dificuldade escolhido afeta a forma como o projeto de cada grupo é avaliado e a cotação máxima que pode ser alcançada (ver Secção 6 deste anunciado).

O projeto prevê 3 entregas. A data final de cada entrega (ou seja, a data de cada entrega) está publicada no site dos laboratórios de SD. 

Dependendo do nível de dificuldade seguido, o faseamento das etapas ao longo do tempo será distinto.

### Faseamento do nível de dificuldade "Bring 'em on!"

#### Entrega 1

  - Etapa A.1

#### Entrega 2

  - Etapas A.2 e B.1

#### Entrega 3

  - Etapas B.2 e C.1

### Faseamento do nível de dificuldade "I am Death incarnate!"

#### Entrega 1

  - Etapas A.1 e A.2

#### Entrega 2

  - Etapas B.1 e B.2

#### Entrega 3

  - Etapas C.1 e C.2




## 4 Processos


### Servidores *TupleSpaces*

Os servidores devem ser lançados recebendo como argumento único o seu porto.
Por exemplo (**$** representa a *shell* do sistema operativo):

`$ mvn exec:java -Dexec.args="3001"`

As interfaces remotas que devem ser usadas para as diferentes implementações do servidor TupleSpaces
 encontram-se definidas nos ficheiros *proto* fornecidos pelo corpo docente juntamente com este enunciado.


### Front-end

O *front-end* é simultaneamente um servidor (pois recebe e responde a pedidos dos clientes) e um cliente 
(pois efetua invocações remotas ao(s) servidore(s) TupleSpaces).
Quando é lançado, recebe o porto em que deve oferecer o seu serviço remoto, assim como os pares de nome de máquina 
e porto dos servidores TupleSpaces com os quais vai interagir (um servidor na variante A, três servidores nas variantes seguintes).

Por exemplo, na etapa 1.2 (ainda sem replicação), o *front-end* pode ser lançado assim para usar o porto 2001 
e ligar-se ao servidor TupleSpaces em localhost:3001:

`$ mvn exec:java -Dexec.args="2001 localhost:3001"`

### Clientes


Os processos cliente recebem comandos a partir da consola. Todos os processos cliente deverão mostrar o símbolo *>* sempre que se encontrarem à espera que um comando seja introduzido.

Para todos os comandos, caso não ocorra nenhum erro, os processos cliente devem imprimir "OK" seguido da mensagem de resposta, tal como gerada pelo método toString() da classe gerada pelo compilador `protoc`, conforme ilustrado nos exemplos abaixo. 

No caso em que um comando origina algum erro do lado do servidor, esse erro deve ser transmitido ao cliente usando os mecanismos do gRPC para tratamento de erros (no caso do Java, encapsulados em exceções). Nessas situações, quando o cliente recebe uma exceção após uma invocação remota, este deve simplesmente imprimir uma mensagem que descreva o erro correspondente.

Os programas de ambos os tipos de clientes recebem como argumentos o nome da máquina e porto onde o _front-end_ do TupleSpace (ou, na etapa 1.1, o servidor TupleSpaces) pode ser encontrado, assim como o *client-id* (ver etapa B.2). Por exemplo, o cliente Java pode ser lançado assim:

`$ mvn exec:java -Dexec.args="localhost:2001 1"`


e o cliente Python pode ser lançado assim:

`$ python3 client_main.py localhost:2001 1`

Para a etapa 2.2 (operação _take_), os programas cliente devem receber como argumento um identificador de cliente
(um inteiro que se pressupõe único entre processos cliente).

Existe um comando para cada operação do serviço: `put`, `read`, `take` e `getTupleSpacesState`. 
Os 3 primeiros recebem 
Uma *string*, delimitada por `<` e `>` e sem conter qualquer espaço entre esses símbolos, que define um tuplo ou, no caso dos comandos `read` e `take`, uma expressão regular (usando a sintaxe das expressões regulares em Java) que especifica o padrão de tuplos pretendidos.

Um exemplo:

```
> put <vaga,sd,turno1>
OK

> put <vaga,sd,turno2>
OK

> take <vaga,sd,turno1>
OK
<vaga,sd,turno1>

> read <vaga,sd,[^,]+>
OK
<vaga,sd,turno2>
```

A partir da etapa B.1, qualquer um dos comandos acima pode receber mais 3 argumentos *opcionais* do tipo inteiro (não negativo). Estes inteiros definem atrasos que  que cada réplica deve aplicar antes de executar o pedido (ver descrição da etapa B.1)

Existem também dois comandos adicionais, que não resultam em invocações remotas: 

-  `sleep`, que bloqueia o cliente pelo número de segundos passado como único argumento.

-  `exit`, que termina o cliente.




## 5 Outras considerações

### Opção de *debug*

Todos os processos devem poder ser lançados com uma opção "-debug". Se esta opção for seleccionada, o processo deve imprimir para o "stderr" mensagens que descrevam as ações que executa. O formato destas mensagens é livre, mas deve ajudar a depurar o código. Deve também ser pensado para ajudar a perceber o fluxo das execuções durante a discussão final.


### Modelo de Interação, Faltas e Segurança


Deve assumir-se que nem os servidores, nem os *front-ends*, nem os clientes podem falhar. 
Deve também assumir-se que as ligações TCP (usadas pelo gRPC) tratam situações de perda, reordenação ou duplicação de mensagens.  
No entanto, as mensagens podem atrasar-se arbitrariamente, logo o sistema é assíncrono. 

Fica fora do âmbito do projeto resolver os problemas relacionados com a segurança (e.g., autenticação dos 
utilizadores, confidencialidade ou integridade das mensagens).


### Persistência

Não se exige nem será valorizado o armazenamento persistente do estado dos servidores.



  

## 6 Avaliação


A avaliação segue as seguintes regras:

- Na primeira entrega, o grupo indica (no documento `README.md` na pasta raíz do seu projeto) qual o nível de dificuldade em que o grupo decidiu trabalhar. 

- Nas entregas seguintes, caso pretenda, o grupo pode baixar o nível de dificuldade (ou seja, passar de "I am Death incarnate!" para "Bring 'em on!"). 
Um grupo que esteja no nível "Bring 'em on!" em qualquer fase do projeto já não poderá subir de nível nas entregas seguintes.

- No final de cada fase, o corpo docente avaliará o conjunto de etapas que são exigidas nessa fase para o nível de dificuldade escolhido 
pelo grupo nesse momento (ver Secção 3).
A classificação obtida pelo grupo nessa fase depende da completude e qualidade do código relevante para esse conjunto de etapas.

- Uma vez avaliada uma etapa no final de uma dada fase, essa etapa já não será reavaliada nas fases seguintes. Por exemplo, se um grupo opta por "I am Death incarnate!" mas submete uma solução incompleta da etapa 1.2 no final da 1ª fase (obtendo uma cotação baixa), 
os pontos perdidos na cotação dessa etapa já não serão recuperados em fases seguintes (mesmo que o grupo complete ou melhore o 
código correspondente, ou mesmo que o grupo baixe de nível de dificuldade).


### Cotações das etapas

A cotação máxima de cada etapa é a seguinte:

- Etapa A.1: 5 valores
- Etapa A.2: 2 valores
- Etapa B.1: 3 valores
- Etapa B.2: 4 valores
- Etapa C.1: 3 valores
- Etapa C.2: 3 valores

### Fotos

Cada membro da equipa tem que atualizar o Fénix com uma foto, com qualidade, tirada nos últimos 2 anos, para facilitar a
identificação e comunicação.

### Identificador de grupo

O identificador do grupo tem o formato `GXX`, onde `G` representa o campus e `XX` representa o número do grupo de SD
atribuído pelo Fénix. Por exemplo, o grupo A22 corresponde ao grupo 22 sediado no campus Alameda; já o grupo T07
corresponde ao grupo 7 sediado no Taguspark.

O grupo deve identificar-se no documento `README.md` na pasta raiz do projeto.

Em todos os ficheiros de configuração `pom.xml` e de código-fonte, devem substituir `GXX` pelo identificador de grupo.

Esta alteração é importante para a gestão de dependências, para garantir que os programas de cada grupo utilizam sempre
os módulos desenvolvidos pelo próprio grupo.

### Colaboração

O [Git](https://git-scm.com/doc) é um sistema de controlo de versões do código fonte que é uma grande ajuda para o
trabalho em equipa.

Toda a partilha de código para trabalho deve ser feita através do [GitHub](https://github.com).

Brevemente, o repositório de cada grupo estará disponível em: https://github.com/tecnico-distsys/GXX-TupleSpaces/ (substituir `GXX` pelo identificador de grupo).

A atualização do repositório deve ser feita com regularidade, correspondendo à distribuição de trabalho entre os membros
da equipa e às várias etapas de desenvolvimento.

Cada elemento do grupo deve atualizar o repositório do seu grupo à medida que vai concluindo as várias tarefas que lhe
foram atribuídas.

### Entregas


As entregas do projeto serão feitas também através do repositório GitHub.

A cada fase estará associada uma [*tag*](https://git-scm.com/book/en/v2/Git-Basics-Tagging).

As *tags* associadas a cada entrega são `SD_Entrega1`, `SD_Entrega2` e `SD_Entrega3`, respetivamente.
Cada grupo tem que marcar o código que representa cada entrega a realizar com uma *tag* específica antes
da hora limite de entrega.

As datas limites de entrega estão definidas no site dos laboratórios: (https://tecnico-distsys.github.io)


### Qualidade do código

A avaliação da qualidade engloba os seguintes aspetos:

- Configuração correta (POMs);

- Código legível (incluindo comentários relevantes);

- [Tratamento de exceções adequado](https://tecnico-distsys.github.io/04-grpc-erros.html);

- [Sincronização correta](https://tecnico-distsys.github.io/02-java-avancado.html);

- Separação das classes geradas pelo protoc/gRPC das classes de domínio mantidas no servidor.

### Instalação e demonstração

As instruções de instalação e configuração de todo o sistema, de modo a que este possa ser colocado em funcionamento,
devem ser colocadas no documento `README.md`.

Este documento tem de estar localizado na raiz do projeto e tem que ser escrito em formato *[
MarkDown](https://guides.github.com/features/mastering-markdown/)*.



### Discussão

As notas das várias partes são indicativas e sujeitas a confirmação na discussão final, na qual todo o trabalho
desenvolvido durante o semestre será tido em conta.

A discussão será precedida por um momento em que se pedirá a todos os membros do grupo que, individualmente, apliquem uma pequena alteração à funcionalidade de seu projeto (implica editar, recompilar, executar para demonstrar). A alteração pedida é de dificuldade muito baixa para quem participou ativamente na programação do projeto, e pode ser realizada em poucas linhas de código.

As notas a atribuir serão individuais, por isso é importante que a divisão de tarefas ao longo do trabalho seja
equilibrada pelos membros do grupo.

Todas as discussões e revisões de nota do trabalho devem contar com a participação obrigatória de todos os membros do
grupo.


**Bom trabalho!**
 
