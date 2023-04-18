# config
DEBUG = True

# render config
SCALE = 1

# tempo
SEC_IN_MICROSECONDS = 10e6

# cor
COR_ACOSTAMENTO = (60, 60, 60)
COR_FAIXA = (15, 15, 15)
COR_DIVISORIA_FAIXA_SENTIDO_IGUAL = (200, 200, 200)
COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE = (200, 180, 60)
COR_DIVISORIA_FAIXA_ACOSTAMENTO = (160, 160, 160)

# tamanho
LARGURA_DIVISORIA = 3
LARGURA_FAIXA = 10
LARGURA_CARRO = 8
COMPRIMENTO_CARRO = 13

# geometria
X = 0
Y = 1
VETOR_RAIZ = [0, 0]
ZERO_DIST = 1e-6

# tipos geometricos
vetor = list[float, float]
point = list[float, float]
segment = list[point, point]
linha = list[point, point]
poligno = list[point]
