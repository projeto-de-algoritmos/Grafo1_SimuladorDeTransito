import json
from enum import Enum
import traceback

from .geometry import point

DEBUG = True


def dprint(*values: object):
    print("[DEBUG]", *values)


def eprint(*values: object, cexit=True):
    traceback.print_stack()
    print("[ERROR]", *values)
    if cexit:
        exit(1)


def enum_list(values: Enum):
    r = []
    for value in values:
        r.append(value.name)
    return sorted(r)


cor = tuple[int, int, int]

Direcao = Enum('Direcao', "normal contrario")
FaixaTipo = Enum('FaixaTipo', "acostamento geral")


class Faixa():
    tipo: FaixaTipo
    sentido: Direcao

    def __init__(self, tipo: FaixaTipo, sentido: Direcao):
        self.tipo = FaixaTipo(tipo)
        self.sentido = Direcao(sentido)


class Pista():
    p1: point
    p2: point
    faixas: list[Faixa]

    def __init__(self, p1: point, p2: point, faixas: list[Faixa]):
        self.p1 = p1
        self.p2 = p2
        self.faixas = faixas


class Carro():
    pista: Pista


class Simulation():
    pistas: list[Pista]
    carros: list[Carro]

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

            pista = Pista(
                p1=pista["p1"],
                p2=pista["p2"],
                faixas=faixas
            )

            pistas.append(pista)

        carros = []

        return pistas, carros

    def read_and_parse_json_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            return data

    def jump_to_next_tick(self):
        pass

    def update(self):
        pass