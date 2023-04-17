import json
from enum import Enum
import traceback

from .geometry import point

DEBUG = False


def dprint(*values: object):
    if DEBUG:
        print("[DEBUG]", *values)


def eprint(*values: object, cexit=True):
    traceback.print_stack()
    print("[ERROR]", *values)
    if cexit:
        exit(1)


def enum_list(values: list[Enum]):
    r = []
    for value in values:
        r.append(value.name)
    return sorted(r)


cor = tuple[int, int, int]

Direcao = Enum("Direcao", "normal contrario")
FaixaTipo = Enum("FaixaTipo", "acostamento geral")


class Faixa:
    pista: "Pista"
    tipo: FaixaTipo
    sentido: Direcao

    def __init__(self, tipo: FaixaTipo, sentido: Direcao):
        self.tipo = FaixaTipo(tipo)
        self.sentido = Direcao(sentido)


class Pista:
    p1: point
    p2: point
    faixas: list[Faixa]

    def __init__(self, p1: point, p2: point, faixas: list[Faixa]):
        self.p1 = p1
        self.p2 = p2
        self.faixas = faixas
        for faixa in self.faixas:
            faixa.pista = self


class Carro:
    pista: Pista
    faixa: Faixa

    nome: str
    posicao: float
    velocidade: float
    destino: point
    velocidade_relativa_maxima_aceitavel: float

    # currently unused
    aceleracao: float

    def __init__(
        self,
        pista: Pista,
        faixa: Faixa,
        nome: str,
        posicao: float,
        velocidade: float,
        destino: point,
        max_rvel: float,
        aceleracao: float,
    ):
        self.nome = nome
        self.pista = pista
        self.faixa = faixa
        self.posicao = posicao
        self.velocidade = velocidade
        self.destino = destino
        self.max_rvel = max_rvel
        self.aceleracao = aceleracao


class Simulation:
    pistas: list[Pista]
    carros: dict[str, Carro]

    running: bool = False

    tick_rate: int

    def __init__(self, cenario_file, tick_rate=60):
        pistas, carros = self.read(cenario_file)
        self.pistas = pistas
        self.carros = carros

        self.running = True

        self.tick_rate = tick_rate

    def get_pistas_and_carros(self):
        return self.pistas, self.carros

    def read(self, cenario_file):
        data = self.read_and_parse_json_file(cenario_file)

        pistas = []

        for pista in data["pistas"]:
            faixas = []
            for faixa in pista["faixas"]:
                faixa_obj = Faixa(
                    FaixaTipo[faixa["tipo"]], Direcao[faixa["sentido"]])
                faixas.append(faixa_obj)

            pista = Pista(p1=pista["p1"], p2=pista["p2"], faixas=faixas)

            pistas.append(pista)

        carros = {}
        dprint(pista.faixas)
        for carro in data["carros"]:
            pista: Pista = pistas[carro["pista"]]
            dprint(pista.faixas, carro["faixa"])
            faixa = pista.faixas[carro["faixa"]]
            nome = carro["nome"]

            carro_obj = Carro(
                nome=nome,
                pista=pista,
                faixa=faixa,
                posicao=carro["posicao"],
                velocidade=carro["velocidade"],
                destino=carro["destino"],
                max_rvel=carro["max_rvel"],
                aceleracao=carro["aceleracao"],
            )

            if carros.get(nome) is not None:
                eprint(f"Carro {nome} já existe!")

            carros[nome] = carro_obj

        return pistas, carros

    def read_and_parse_json_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            return data

    def jump_to_next_tick(self):
        pass

    def update(self):
        pass
