# Simulador De Trânsito

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: Projetos de Algoritmos<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 18/0027239  |  Renato Britto Araujo |
| xx/xxxxxx  |  xxxx xxxx xxxxx |

## Sobre 

### Simulação

O objetivo do projeto é **calcular a estratégia ótima que carros dirigindo em pistas irão adotar em múltiplos cenários adversariais** (todos contra todos). Atingidos esse objetivos, isso nos permite analisar e teorizar heurísticas para decisões efetivas num contexto de trânsito, sendo o projeto um estudo de teoria dos jogos.

Isso é feito a partir de um processo de **simulação**. Cada carro possui parâmetros de como irá dirigir (por exemplo, a velocidade máxima que ele se sente confortável em acelerar dentro da via), e o projeto **assume que todos os carros querem chegar ao seu destino o mais rápido possível**.

As decisões que um carro pode tomar são:
- Virar para esquerda.
- Virar para direita.
- Seguir para outra pista caso a possibilidade esteja presente.
- 

Para cada passo da simulação, cada carro irá **assumir que cada outro carro não irá mudar seu atual estado atual** (ou seja, vai continuar seguindo em frente sem virar, mesmo se houver um carro mais devagar na frente). Com isso, é possível prever exatamente como o "futuro" de cada passo da simulação na perpectiva de um carro em específico será. Com isso, cada carro faz um **BFS** no seu espaço de possibilidades até descobrir qual caminho custa menos passos (por isso o BFS é usado) para decidir sua ação no presente momento. O nome atribuído à essa decisão é de: ***decisão ótima local*** (uma única decisão ótima local requer muita computação para ser calculada).

Todos os carros tomam uma decisão ótima local a cada passo da simulação, e cada uma dos carros não prioriza conceitos considerados arcaicos como "segurança" ou "respeito". Sendo assim, um contexto anárquico acontece, e todos os carros adotam a SUA melhor estratégia a cada momento.

É necessário calcular estratégias ótimas locais pois não é possível que um carro saiba o que acontecerá no futuro. Além disso, existe uma quantidade grande de computações que são complexas demais para otimizar de forma assintótica, tornando esse projeto perfeito para o contexto.

### Fatores técnicos

Pela alta quantidade de computação e baixa prioridade de desenvolvimento em performance, os cenários desse projeto precisarão ser curtos, com fim de evitar uma demora significativa no cálculo do resultado.

Além disso, existe um parâmetro chamado de ***tick***, que indica quantos milissegundos de simulação cada passo irá tomar. Quanto mais segundos, menos intesa é a computação porque menos passos são calculados.

A configuração é feita a partir de uma arquivo json. No geral, criar uma configuração nova requer algum esforço, e portanto recomenda-se usar alguma dos cenários na pasta `cenarios/`. Cada arquivo de cenário possui um título descritivo do que ele representa. Digite `./set_cenario CENARIO=cenario/{nome_do_cenario}.json` para adicionar a configuração desejada (ou copie manualmente).  

O projeto também contem um possui uma interface gráfica, onde a simulação é executava visualmente para ficar intuitivo o uso.

### Informações secundárias (lê se quiser kk)

A velocidade máxima que um carro estará é dada pela função `velocidade_relativa_maxima_aceitavel * velocidade_da_via`, sendo assim a velocidade da pista influenciará todos os carros.

Essa parametrização dos atributos da simulação nesse projeto foi feito à partir do tempo que gastei no trânsito vindo para a faculdade. Ou seja, tentei minimizar o número de parâmetros aqui sem detraír valor da qualidade da simulação. E a qualidade da simulação é razoável porque fiz um processo de [wargaming](https://www.rand.org/topics/wargaming.html) dos processos que acontecem na vida real no trânsito antes de começar o projeto.

Uma potencial expansão do projeto seria incluir na decisão ótima local um certo nível de iterações de cálculo da decisão ótima local de outros carros. Ou seja, cada carro calculará uma decisão ótima local mais simples para cada outro carro durante cada passo da simulação separadamente (como um motorista faria). Claramente, a complexidade assintótica disso é alta demais e preferi não o fazer.

## Screenshots
<!-- Adicione 3 ou mais screenshots do projeto em funcionamento. -->

## Instalação 
**Linguagem**: Python3<br>
**Framework**: Pygame<br>

<!-- Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários. -->

## Uso 
<!-- Explique como usar seu projeto caso haja algum passo a passo após o comando de execução. -->

## Outros 
<!-- Quaisquer outras informações sobre seu projeto podem ser descritas abaixo. -->




