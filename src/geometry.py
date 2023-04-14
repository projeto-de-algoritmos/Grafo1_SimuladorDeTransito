import math

X = 0
Y = 1
VETOR_RAIZ = [0,0]

vetor = list[int,int]
point = list[int, int]
segment = list[point, point]
linha = list[point, point]
poligno = list[point]

def distancia_euclidiana(p1: point, p2: point):
    return math.sqrt((p1[X] - p2[X]) ** 2 + (p1[Y] - p2[Y]) ** 2)


def ponto_de_aproximacao_maxima_ponto_de_segmento(l: segment, p: point):
    raise NotImplementedError


def encontro_linha_linha(l2: linha, l1: linha):
    raise NotImplementedError


def encontro_segmento_segmento(l2: linha, l1: linha):
    raise NotImplementedError


def rotacionar_vetor_horario(v: point, rad: float = math.pi/2, ref: point = [0, 0]):
    v[X] -= ref[X]
    v[Y] -= ref[Y]

    x = v[X] * math.cos(rad) - v[Y] * math.sin(rad)
    y = v[X] * math.sin(rad) + v[Y] * math.cos(rad)

    return [x+ref[X], y+ref[Y]]


def get_angulo_entre_p1_e_p2(p1: point, p2: point):
    ang = math.atan2(p2[Y] - p1[Y], p2[X] - p1[X])
    if ang < 0:
        ang += 2*math.pi
    return ang


def rad_pra_deg(rad: float):
    return round(rad * 180 / math.pi, ndigits=2)


def deg_pra_rad(deg: float):
    return round(deg * math.pi / 180.0, ndigits=2)


def normalizar_vetor(v: point, base: point = [0, 0]):
    nv = [v[X] - base[X], v[Y] - base[Y]]
    nv[X] /= distancia_euclidiana(base, v)
    nv[Y] /= distancia_euclidiana(base, v)
    return [nv[X] + base[X], nv[Y] + base[Y]]


def get_vetor(p1: point, p2: point):
    return [p2[X] - p1[X], p2[Y] - p1[Y]]


def multiplica_vetor(v: point, n: float):
    return [v[X] * n, v[Y] * n]


def soma_vetor(v1: point, v2: point):
    return [v1[X] + v2[X], v1[Y] + v2[Y]]


if __name__ == "__main__":
    v = rotacionar_vetor_horario([1, 0], deg_pra_rad(30), [0, 0])

    print("deveria dar [0.8678191796776499, 0.49688013784373675]")
    print(v)

    print("\ndeveria dar 29.79")
    print(rad_pra_deg(get_angulo_entre_p1_e_p2([0, 0], v)))

    print(
        "\ndeveria dar 3.1181980230142936 [0.5990059534038413, 0.8007445708756039] 1.0")
    nv = [v[X] + 1, v[Y] + 2]
    print(distancia_euclidiana([0, 0], nv), normalizar_vetor(
        nv), distancia_euclidiana([0, 0], normalizar_vetor(nv)))
