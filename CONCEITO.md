## Wikipedia Crossreferencer

- Já começei e tem um código decente.
- Grafos são naturalmente aplicáveis

## Simulador de Caminho Ótimo no Transito (Teoria dos Jogos)

- começar do zero
- tem q ter algum visual
- como q vai ir grafos nisso? (BFS, DFS)
- puxar dados geográficos de pista (ia ser divertido)

Conceito do problema à se resolver

```json
{
  "pistas": [
    {
      "p1": [10, 20],
      "p2": [10, 1000],
      "direcao": "leste",
      "faixas": [
        {
            "name": "acostamento",
            "relativo": "norte",
        },
        {
            "name": "geral",
            "sentido": "leste",
            "relativo": "norte",
        },
        {
            "name": "acostamento",
            "relativo": "norte",
        },
      ]
    }
  ],
  "carros": [
    {
      "nome": "outro motorista",
      "pista": 0,
      "posição": [10, 25],
      "velocidade": [0, 11.11],
      "destino": [10, 1000],
      "personalidade": "segurança acima de tudo",
      "vingativo": true,
      "velocidade_relativa_aceitavel": 1.2,
      "aceleracao": "4.0"
    }
  ],
  "player": {
    "nome": "player",
    "pista": 0,
    "posição": [10, 20],
    "velocidade": [0, 16.66],
    "destino": [10, 1000],
    "personalidade": "seleção natural impera",
    "vingativo": false,
    "velocidade_relativa_aceitavel": 1.8,
    "aceleracao": "8.333"
  }
}
```

O programa deve ser capaz de dar instruções em texto do que deveria ser feito.

Temos 2 carros em uma pista de faixa única indo do oeste ao leste.

Todos os carros médios tem 4 metros de comprimento.

O player está a 1 metro do carro à frente.

O carro à frente está dirigindo mais devagar do que o player.

Uma simulação no espaço de possibilidade deve ser realizada.

Todos os carros tem possibilidade de:
- Ir pra faixa da esquerda (se possível)
- Ir pra faixa da direita (se possível)
- Acelerar (se colisão for evitada)
- Freiar
- Virar à esquerda (se houver ramifição da pista à esquerda)
- Virar à direita (se houver ramificação da pista à direita)

Note como algumas ações são mutualmente exclusivas.

A cada segundo (da simulação), cada player calcula sua melhor estratégia dado o cenário do jogo pra chegar ao seu destino, e executa a ação.

O próximo passo é escolhido por cada carro baseado numa busca DFS ou BFS (à determinar sistema correto).

No caso acima, o que deveria ser feito seria o ato totalmente seguro e recomendado de
ultrapassar pelo acostamento.

## Poker Oracle

- Joga uma partida de poker contra máquina, onde você pode usar análises complexas de jogadas (e a máquina também)
- Parece mais complicado do que parece
- Precisa de DFS ou BFS pra fazer isso mesmo?
