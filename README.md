# Simulador De Trânsito

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: Projetos de Algoritmos<br>

## Alunos
| Matrícula  | Aluno                |
| ---------- | -------------------- |
| 18/0027239 | Renato Britto Araujo |
| xx/xxxxxx  | xxxx xxxx xxxxx      |

## Sobre 

### Simulação

O objetivo do projeto é **calcular a estratégia ótima que carros dirigindo em pistas irão adotar em múltiplos cenários adversariais** (todos contra todos). Atingidos esse objetivos, isso nos permite analisar e teorizar heurísticas para decisões efetivas num contexto de trânsito, sendo o projeto um estudo de teoria dos jogos.

Isso é feito a partir de um processo de **simulação**. Cada carro possui parâmetros de como irá dirigir (por exemplo, a velocidade máxima que ele se sente confortável em acelerar dentro da via), e o projeto **assume que todos os carros querem chegar ao seu destino o mais rápido possível**.

As decisões que um carro pode tomar são apenas 3, cada uma caso a possibilidade se faça presente:
- Virar para esquerda.
- Virar para direita.
- Seguir para outra pista.

Para cada passo da simulação, cada carro irá **assumir que cada outro carro não irá mudar seu atual estado atual** (ou seja, vai continuar seguindo em frente sem virar, mesmo se houver um carro mais devagar na frente). Com isso, é possível prever exatamente como o "futuro" de cada passo da simulação na perpectiva de um carro em específico será. Com isso, cada carro faz um **BFS** no seu espaço de possibilidades até descobrir qual caminho custa menos passos (por isso o BFS é usado) para decidir sua ação no presente momento. O nome atribuído à essa decisão é de: ***decisão ótima local*** (uma única decisão ótima local requer muita computação para ser calculada).

Todos os carros tomam uma decisão ótima local a cada passo da simulação, e cada uma dos carros não prioriza conceitos considerados arcaicos como "segurança" ou "respeito". Sendo assim, um contexto anárquico acontece, e todos os carros adotam a SUA melhor estratégia a cada momento.

É necessário calcular estratégias ótimas locais pois não é possível que um carro saiba o que acontecerá no futuro. Além disso, existe uma quantidade grande de computações que são complexas demais para otimizar de forma assintótica, tornando esse projeto perfeito para o contexto.

### Fatores técnicos

Pela alta quantidade de computação e baixa prioridade de desenvolvimento em performance, os cenários desse projeto precisarão ser curtos, com fim de evitar uma demora significativa no cálculo do resultado.

Além disso, existe um parâmetro chamado de ***tick***, que indica quantos milissegundos de simulação cada passo irá tomar. Quanto mais segundos, menos intesa é a computação porque menos passos são calculados.

O cenário é feita a partir de um arquivo json. No geral, criar um cenário novo requer algum esforço, e portanto recomenda-se usar algum dos cenários na pasta `cenarios/`. Cada arquivo de cenário possui um título descritivo do que ele representa. Digite `make load_cenario file=cenario/{nome_do_cenario}.json` para adicionar o cenário desejado (ou copie manualmente).  

O projeto também contem um possui uma interface gráfica, onde a simulação é executava visualmente para ficar intuitivo o uso.

### Informações secundárias (lê se quiser kk)

A velocidade máxima que um carro estará é dada pela função `velocidade_relativa_maxima_aceitavel * velocidade_da_via`, sendo assim a velocidade da pista influenciará todos os carros.

Essa parametrização dos atributos da simulação nesse projeto foi feito à partir do tempo que gastei no trânsito vindo para a faculdade. Ou seja, tentei minimizar o número de parâmetros aqui sem detraír valor da qualidade da simulação. E a qualidade da simulação é razoável porque fiz um processo de [wargaming](https://www.rand.org/topics/wargaming.html) dos processos que acontecem na vida real no trânsito antes de começar o projeto.

Uma potencial expansão do projeto seria incluir na decisão ótima local um certo nível de iterações de cálculo da decisão ótima local de outros carros. Ou seja, cada carro calculará uma decisão ótima local mais simples para cada outro carro durante cada passo da simulação separadamente (como um motorista faria). Claramente, a complexidade assintótica disso é alta demais e preferi não o fazer.

O programa deve ser capaz de dar instruções em texto do que deveria ser feito.

Todos os carros médios tem 4 metros de comprimento.
Todos os carros mantem um distância mínima de 1 metro.
Todos os carros calculam e mudam de velocidade instantaneamenete.

## Screenshots
<!-- Adicione 3 ou mais screenshots do projeto em funcionamento. -->

## Instalação 
**Linguagem**: Python3<br>
**Framework**: Pygame<br>

<!-- Descreva os pré-requisitos para rodar o seu projeto e os comandos necessários. -->

## Uso 

### Configurar ambiente

Você pode usar um virtual environment ou rodar na sua máquina instalando o pacote diretamente de com pip.

```
pip install -r requirements.txt
```

Dependências: `pygame`.

### Executar

Basta rodar:

```bash
python src/main.py
```

Ou

```bash
make run
```

Note que o cenário carregado no arquivo `cenario.json` por padrão pode ser inválido.

### Gerenciar cenários

Ver cenários
```
make list_cenarios
```

Carregar um cenário
```
make load_cenario file=cenario/{nome_do_cenario}.json  
```

Salvar um cenário
```
make save_cenario file=cenario/{nome_do_cenario}.json
```

## Outros 

[TODO]
- Trocar sistema de pista retangular por pontos. (cada pista é representada por uma linha, e o renderizador se dá o trabalho de calcular o retângulo)
- O renderizador faz pistas diagonais. Agora a direção dos carros não será leste ou oeste, e sim posição relativa na própria pista.
- Criar sistema simulador
- Sistema de simulação consegue fazer o parse das pistas que se conectam em algum ponto.
- Desenhar carro como dependente da pista em que está.
- Criar interaface gráfica com seguintes operações:
  - Pausar/Resumir a simulação
  - Botão para adicionar novo carro (clica em alguma faixa e o carro aparece)
  - Botão para adicionar nova pista (de onde até onde, e incluir representação se pista conecta ou não com outra pista)

[IGNORE]



