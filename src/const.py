# config
DEBUG = True

# tempo EM MICROSSEGUNDOS
SEC_IN_MICROSECONDS = 10e6

# cor EM TUPLE(R,G,B)
COR_ACOSTAMENTO = (60, 60, 60)
COR_FAIXA = (15, 15, 15)
COR_DIVISORIA_FAIXA_SENTIDO_IGUAL = (200, 200, 200)
COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE = (200, 180, 60)
COR_DIVISORIA_FAIXA_ACOSTAMENTO = (160, 160, 160)
COR_CARRO_COMPLETO = (0, 255, 0, 0.1)


# tamanho visual (da renderização)
def scaled(x):
    global SCALE
    return x * SCALE


# tamanho físico (da simulação) EM METROS
LARGURA_DIVISORIA = 1
LARGURA_FAIXA = 3
LARGURA_CARRO = 2
COMPRIMENTO_CARRO = 5  # metros
DISTANCIA_MINIMA_CARRO_A_FRENTE = 1  # metros
FATOR_AJUSTE_CARRO_VISUAL = 0.3

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

# restrições da simulacao
DEFAULT_TICK_RATE = 60  # ms
DEFAULT_TICK = 1000 / 60  # ms
MAX_SIM_ITER_COUNT = 4

# precisão de calculos
FATOR_ARRENDONDAMENTO = 0.5
