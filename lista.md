# 1

- a,b,c,d,e,f
- a,b,d,c,e,f
- a,b,d,e,c,f
- a,d,b,c,e,f
- a,d,b,e,c,f
- a,d,e,b,c,f

Existem 6 ordenações topológicas.

# 2

```python
def main():
    n = int(input())
    ne = int(input())
    e = [[] for i in range(n)]
    inc = [0 for i in range(n)]
    for i in range(ne):
        u,v = input().split(" ")
        u = int(u) - 1
        v = int(v) - 1
        inc[v] = 1
        e[u].append(v)

    c = has_cycle(n, e)
      print(*c)

def has_cycle(n, e):
    q = []
    p = [0 for i in range(n)]
    for v in range(n):
        p = [0 for i in range(n)]
        c = it(v, e, p, q)
        if c != -1:
            while q[0] != c:
                q[1:]
            return q
    return None

def it(n, e, p, q):
    print(n+1, q)

    if p[n] == 1:
        p[n] = 2
        return n
    
    p[n] = 1
    q.append(n)
    for v in e[n]:
        x = it(v, e, p, q)
        return x

    q.pop()
    if p[n] == 2:
        return n
    return -1

main()
```

# 3

```python
def main():
    n = int(input())
    ne = int(input())
    e = [[] for i in range(n)]
    inc = [0 for i in range(n)]
    for i in range(ne):
        u,v = input().split(" ")
        u = int(u) - 1
        v = int(v) - 1
        inc[v] = 1
        e[u].append(v)

    c = has_cycle(n, e)
    if c:
        print(*c)
    dag = []
    # se não ha ciclos, temos uma dag necessariamente

    for i in inc:
        if inc[i] == 0:
            print(get_dag(i, e, []))

def get_dag(n, e, dag):
    print("get_dag", n, e, dag)
    dag.append(n)
    for m in e[n]:
        get_dag(m, e, dag)
    return dag

def has_cycle(n, e):
    q = []
    p = [0 for i in range(n)]
    for v in range(n):
        p = [0 for i in range(n)]
        c = it(v, e, p, q)
        if c != -1:
            while q[0] != c:
                q[1:]
            return q
    return None

def it(n, e, p, q):
    print(n+1, q)

    if p[n] == 1:
        p[n] = 2
        return n
    
    p[n] = 1
    q.append(n)
    for v in e[n]:
        x = it(v, e, p, q)
        return x

    q.pop()
    if p[n] == 2:
        return n
    return -1

main()
```

# 4

...

# 5

Suponha uma árvore binária com 1 nó.
Ela possui 1 raiz e nenhum nó com 2 filhos.

Agora vamos adicionar um nó. Este nó só pode ser inserido em 2 espaços:
- Como filho de nó com 0 filhos
- Como filho de nó com 1 filho

Caso o nó tenha 0 filhos, o numero de raizes não mudará, e o número de nós com 2 filhos também não.

Caso o nó tenha 1 filho, o número de raizes cresce em 1, e o número de nó com 2 filhos também cresce 1.

Portanto, o número de nós com 2 filhos sempre será um número menor que o número de nós raíz.

# 6

...

# 7

Cada dispositivo estará a uma distância `<= R`, o que os conecta.

Os dispositivos formam um grafo G.

Para que o grafo G (a rede) **não** esteja conectada, o grafo precisa ter ao menos 2 grupos de dispositivos separados por distância `> R`, ou seja, dois ou mais componentes fortemente conectados.

Vamos supor que existam 2 componentes fortemente conectados no grafo G, onde iremos analisar os vizinhos de um nó que faz parte do componente com o menor número de elementos.

Este nó precisaria estar a distância `> R` para, ao menos, `floor((N-1)/2)` nós, porque o outro grupo é maior que o grupo deste nó, e este grafo possui 2 componentes fortemente conectados.

Mas, sabemos que as propriedades forçam os vizinhos `<= R` a serem `N/2`, sendo `N` um número par.

E sabemos que `floor((N-1)/2) < N/2` quando `N` é par. Isso é uma contradição.

Portanto é **impossível** existirem 2 ou mais componentes fortemente conectados no grafo G. Apenas um único componente fortemente conectado pode existir, o que significa que a rede está conectada.

# 8

...

# 9

O grafo G, possui `N` nós, onde N é um número natural `> 2`. 

Existem 2 nós `s` e `t` em que o número de arestas que forma o menor caminho `s-t` é `> floor(N/2)`.

Ou seja, o número de nós no seu caminho é igual a `floor(N/2)`.

Para demonstrar que existe algum nó `V` cujo qual sua remoção levaria a dois componentes fortemente conectados, vamos assumir que analisaremos cada um dos nós intermediários no caminho `s-t`.

Os nós intermediários podem ser ordenados por sua posição no menor caminho `s-t`, o primeiro vizinho de `s` seria o `V1`, o segundo `V2`... Representamos como `Vm`.

A menor distância de `Vm` até `s` é sempre `m`.
A menor distância de `Vm` até `t` é sempre `|V| - m + 1`.

...


```python

```

# 10

...

# 11

...

# 12

...