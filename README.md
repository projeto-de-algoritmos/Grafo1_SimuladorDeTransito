# Simulador De Trânsito

**Número da Lista**: 5 (T02)<br>
**Conteúdo da Disciplina**: Projetos de Algoritmos<br>

## Alunos
| Matrícula  | Aluno                |
| ---------- | -------------------- |
| 18/0027239 | Renato Britto Araujo |

## Sobre 

"[...] dispusestes tudo com **medida, quantidade e peso**" - Sabedoria 11:20, Bíblia Católica.

## Screenshots

*Execução do exemplo do cenário T1*

![pa_g2](https://user-images.githubusercontent.com/45462822/235490452-987bafa9-0be6-4870-a414-874a4500001c.gif)


*Execução do exemplo do cenário T2*

![pa_g1](https://user-images.githubusercontent.com/45462822/235490452-987bafa9-0be6-4870-a414-874a4500001c.gif)


*Execução do exemplo do cenário T3*

![pa_g3](https://user-images.githubusercontent.com/45462822/235490452-987bafa9-0be6-4870-a414-874a4500001c.gif)



### Nota para o avaliador

No arquivo `src/sim.py`, função `prever_melhor_jogada()`, você pode encontrar o DFS, que seria o objetivo do projeto.

### Simulação

O objetivo do projeto é **calcular a estratégia ótima que carros dirigindo em pistas irão adotar em múltiplos cenários adversariais** (todos contra todos). Atingidos esse objetivos, isso nos permite analisar e teorizar heurísticas para decisões efetivas num contexto de trânsito, sendo o projeto um estudo de teoria dos jogos.

Isso é feito a partir de um processo de **simulação**. Cada carro possui parâmetros de como irá dirigir (por exemplo, a velocidade máxima que ele se sente confortável em acelerar dentro da via), e o projeto **assume que todos os carros querem chegar ao seu destino o mais rápido possível**.

As decisões que um carro pode tomar são apenas 3, cada uma caso a possibilidade se faça presente:
- Virar para esquerda.
- Virar para direita.
- Seguir para outra pista.

Para cada passo da simulação, cada carro irá **assumir que cada outro carro não irá mudar seu atual estado atual** (ou seja, vai continuar seguindo em frente sem virar, mesmo se houver um carro mais devagar na frente). Com isso, é possível prever exatamente como o "futuro" de cada passo da simulação na perpectiva de um carro em específico será. Com isso, cada carro faz um **DFS** no seu espaço de possibilidades até descobrir qual caminho custa menos passos para decidir sua ação no presente momento. O nome atribuído à essa decisão é de: ***decisão ótima local*** (uma única decisão ótima local requer muita computação para ser calculada).

Todos os carros tomam uma decisão ótima local a cada passo da simulação, e cada uma dos carros não prioriza conceitos considerados arcaicos como "segurança" ou "respeito". Sendo assim, um contexto anárquico acontece, e todos os carros adotam a SUA melhor estratégia a cada momento.

É necessário calcular estratégias ótimas locais pois não é possível que um carro saiba o que acontecerá no futuro. Além disso, existe uma quantidade grande de computações que são complexas demais para otimizar de forma assintótica, tornando esse projeto perfeito para o contexto.

### Fatores técnicos

Pela alta quantidade de computação e baixa prioridade de desenvolvimento em performance, os cenários desse projeto precisarão ser curtos, com fim de evitar uma demora significativa no cálculo do resultado.

Além disso, existe um parâmetro chamado de ***tick***, que indica quantos milissegundos de física da simulação cada passo irá tomar. Quanto mais segundos, menos intesa é a computação porque menos passos são calculados.

O cenário é feita a partir de um arquivo json. No geral, criar um cenário novo requer algum esforço, e portanto recomenda-se usar algum dos cenários na pasta `cenarios/`. Cada arquivo de cenário possui um título descritivo do que ele representa. Digite `make load_cenario file=cenario/{nome_do_cenario}.json` para adicionar o cenário desejado (ou copie manualmente).  

O projeto também possui uma interface gráfica, onde a simulação é executava visualmente para ficar intuitivo o uso.

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

### As verdadeiras leis do trânsito

Leia a palavra 'lei' como as leis de newton, não como as leis do código penal.

- Lei 1: Todo carro irá dirigir na maior velocidade que puder dentro do seu limite de conforto.
  - É possível que o limite de conforto supere a velocidade máxima do próprio carro.
- Lei 2: A velocidade de um carro que está atrás de outro carro na mesma faixa sempre será a velocidade do carro da frente.
  - Caso um carro esteja imediatamente atrás de outro, a velocidade desejada do carro atrás é sempre maior ou igual ao carro da frente. 
  - Sendo assim, é possível que a definição da velocidade de um carro depende da velocidade de um grupo formado pela sequência de outros carros à sua frente. 
  - Este grupo pode estar em um cenário onde a sequência dê uma volta completa até o carro original. Ou seja, um ciclo.
  - No caso de ciclos, a velocidade dos carros no ciclo é igual a velocidade do carro que dirige mais devagar dentro do ciclo.
- Lei 3: Um carro sai de sua faixa com o propósito exclusivo de chegar ao seu destino mais rápido. 
- Lei 4: Pistas podem ser classificadas de duas formas na perspectiva de um carro em específico: ela existe ou não. 
  - Um sinal que se fecha durante o trajeto de um carro é equivalente à inexistencia temporária de uma pista.
- Lei 5: Caso ocorra uma parada na pista, carros irão se distribuir por todas faixas de forma uniforme.
- Lei 6: Caso não exista forma de um carro chegar ao seu destino, ele irá freiar.

### Informações Adicionais

A velocidade máxima que um carro estará é dada pela função `velocidade_relativa_maxima_aceitavel * velocidade_da_via`, sendo assim a velocidade da pista influenciará todos os carros. Ni cenário, a chave que indica a velocidade relativa máxima aceitável é `max_rvel`.

Essa parametrização dos atributos da simulação nesse projeto foi feito à partir do tempo que gastei no trânsito vindo para a faculdade. Ou seja, tentei minimizar o número de parâmetros aqui sem detraír valor da qualidade da simulação. E a qualidade da simulação é razoável porque fiz um processo de [wargaming](https://www.rand.org/topics/wargaming.html) dos processos que acontecem na vida real no trânsito antes de começar o projeto.

Uma potencial expansão do projeto seria incluir na decisão ótima local um certo nível de iterações de cálculo da decisão ótima local de outros carros. Ou seja, cada carro calculará uma decisão ótima local mais simples para cada outro carro durante cada passo da simulação separadamente (como um motorista faria). Claramente, a complexidade assintótica disso é alta demais e preferi não o fazer.

O programa deve ser capaz de dar instruções em texto do que deveria ser feito.

Todos os carros médios tem 4 metros de comprimento.
Todos os carros mantem um distância mínima de 1 metro.
Todos os carros calculam e mudam de velocidade instantaneamenete.
A posição de um carro é dada pela sua frente.

### Configuração do app

É feita com injeção de dependências na main. Os parametros estão em `config.json`.

### Descrição da configuração

- **resolution**: [resolucao X da tela, resolucao X da tela]
- **render_scale**: multiplica a resolucao dentro do programa. se X = 100, render_scale = 3, 'X' virtual é de 300
- **fullscreen**: está em tela cheia
- **max_fps**: fps máximo (quanto mais, mais o computador vai se esforçar pra reproduzir a simulação)
- **tick**: milissegundos entre cada passo da simulação (taxa de atualização da física)
- **cenario_file**: nome do arquivo de cenário
- **prever_jogada_cooldown**: número de vezes evitará recalcular rota de um carro com tentativa recente
- **skip_prever_jogada_for_ms**: pula previsão de jogadas nos primeiros milissegundos de exceução, para observar-mos o que ocorre logo nas primeiras decisões visualmente.

### Lista de tarefas

[TODO v1]
- [SIM] Consertar carros ocupando a mesma faixa
- [SIM] Amortizar mais os cáculos
- [SIM] Permitir que um carro chegue a seu destino na mesma pista onde está.
- [SIM] Lidar com possibilidade de usar acostamentos e ultrapassagens por faixa sentido oposto
- [GRAFO] Adicionar metodo de conectar estradas (incluindo uma pista que se conecta com outra de forma indireta)
- [SIM] Detector de caminhos possíveis (disjoint set union)

[TODO later]
- [REN] Consertar sistema de render_scale mal feito e inconsistente.
- [SIM] Detector de ciclos de carros engarrafados
- [GUI] Criar interaface gráfica com seguintes operações:
  - [GUI] Pausar/Resumir a simulação
  - [GUI] Botão para adicionar novo carro (clica em alguma faixa e o carro aparece)
  - [GUI] Botão para adicionar nova pista (de onde até onde, e incluir representação se pista conecta ou não com outra pista)

[IGNORE v1]
- [v1] Não faça NENHUMA otimização de performance até que a necessidade exista
  - Sim, vai explorar todo o ambiente de possibilidades.
  - Caso encontre uma solução, pare a exploração (ou seja, todas os passos devem consumir o mesmo "tempo" para poder parar na primeira solução).
  - Caso demore demais, decida baseado no limite máximo de exploração
  - Uma solução impossível = Uma solução que demorou demais.




### Falhas do modelo

[v1]
- Quando carro chega ao seu objetivo, ele desaparece
- Sem retornos
- Sem aceleração
- Instantaneamente muda de faixa pra voltar
- Acostamento é só elemento visual  
- Não existe pardal
- Não existe sinal
- Não se freia antes de curvas acentuadas
- Não acontecem acidentes
- O tempo de reação de cada carro é igual ao tick_rate da simulação.
