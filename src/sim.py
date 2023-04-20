import json
from enum import Enum
import traceback
import copy

from .geometry import *
from .gui import *
from .const import *
from .algoritmos import *


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
    carros: list["Carro"]

    def __init__(
        self, p1: point, p2: point, faixas: list[Faixa], carros: list["Carro"]
    ):
        self.p1 = p1
        self.p2 = p2
        self.faixas = faixas
        for faixa in self.faixas:
            faixa.pista = self
        self.carros = carros
        for carro in self.carros:
            carro.pista = self
            carro.faixa = self.faixas[carro.faixa_i]

        self.validate()

    def get_comprimento(self):
        return distancia_euclidiana(self.p1, self.p2)

    def validate(self):
        conds: list[bool] = [
            self.p1[X] < 0,
            self.p2[X] < 0,
            self.p1[Y] < 0,
            self.p2[Y] < 0,
        ]
        for cond in conds:
            if cond:
                eprint("Pista fora do mapa")


class Local:
    pista: int
    faixa: int
    posicao: float

    def __init__(self, pista: int, faixa: int, posicao: float):
        self.pista = pista
        self.faixa = faixa
        self.posicao = posicao


class Carro:
    # constantes
    nome: str
    cor: str
    velocidade: float
    velocidade_relativa_maxima_aceitavel: float
    local_origem: Local
    local_destino: Local
    aceleracao: float  # [TODO] usar isso

    # serão alteradas durante a simulação
    pista_i: int
    faixa_i: int
    posicao: float
    pista: Pista
    faixa: Faixa

    def __init__(
        self,
        nome: str,
        cor: str,
        velocidade: float,
        max_rvel: float,
        aceleracao: float,
        local_origem: Local,
        local_destino: Local,
    ):
        self.nome = nome
        self.cor = cor
        self.velocidade = velocidade
        self.max_rvel = max_rvel
        self.aceleracao = aceleracao
        self.local_origem = local_origem
        self.local_destino = local_destino

        self.pista_i = local_origem.pista
        self.faixa_i = local_origem.faixa
        self.posicao = local_origem.posicao


# [TODO] Fazer adapter grafo-simulacao?


class Simulation:
    pistas: list[Pista]
    carros: dict[str, Carro]

    running: bool = False

    tick_rate: int

    grafo_pista: Grafo

    def __init__(self, cenario_file, tick_rate=60):
        pistas, carros = self.read(cenario_file)
        self.pistas = pistas
        self.carros = carros

        self.running = True

        self.tick_rate = tick_rate
        self.calc = {}

    def get_pistas_and_carros(self):
        return self.pistas

    def read(self, cenario_file):
        data = self.read_and_parse_json_file(cenario_file)

        pistas = []
        carros: dict[str, Carro] = {}

        for carro in data["carros"]:
            nome = carro["nome"]

            origem = Local(
                carro["origem"]["pista"],
                carro["origem"]["faixa"],
                carro["origem"]["posicao"],
            )

            destino = Local(
                carro["origem"]["pista"],
                carro["origem"]["faixa"],
                carro["origem"]["posicao"],
            )

            if carros.get(nome) is not None:
                eprint(f"Carro {nome} já existe!")

            carro_obj = Carro(
                nome=nome,
                cor=carro["cor"],
                velocidade=carro["velocidade"],
                max_rvel=carro["max_rvel"],
                aceleracao=carro["aceleracao"],
                local_origem=origem,
                local_destino=destino,
            )

            carros[nome] = carro_obj

        for i in range(len(data["pistas"])):
            pista = data["pistas"][i]
            faixas = []
            for faixa in pista["faixas"]:
                faixa_obj = Faixa(FaixaTipo[faixa["tipo"]], Direcao[faixa["sentido"]])
                faixas.append(faixa_obj)

            pista_carros = list(
                filter(lambda carro: i == carro.pista_i, carros.values())
            )

            pista = Pista(
                p1=pista["p1"], p2=pista["p2"], faixas=faixas, carros=pista_carros
            )

            pistas.append(pista)

        return pistas, carros

    def contruir_grafo_pistas(self, pistas):
        pass

    def read_and_parse_json_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            return data

    def jump_to_next_tick(self):
        pass

    def update(self):
        for carro in self.carros.values():
            velocidade = self.get_carro_velocidade(carro)

            carro.posicao += velocidade / self.tick_rate

            if carro.posicao > carro.pista.get_comprimento() - COMPRIMENTO_CARRO:
                carro.posicao = 0

    def get_carro_velocidade(self, carro: Carro) -> float:
        velocidade_baseline = self.get_carro_velocidade_baseline(carro)

        bloqueado, next_carro = self.is_carro_bloqueando_movimento(carro)
        if not bloqueado:
            return velocidade_baseline

        return self.get_carro_velocidade(next_carro)

    def is_carro_bloqueando_movimento(self, c_carro) -> tuple[bool, Carro]:
        # verifique se existe algum carro dentro do espaço de movimento do carro atual
        # o carro atual.
        # O bloqueio é definido por um carro que compartilha a mesma faixa e está
        # em algum lugar entre [0,5] metros da posição do carro atual na faixa.
        p = c_carro.posicao
        intervalo = [p, p + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE]
        for carro in self.carros.values():
            if carro == c_carro or carro.faixa != c_carro.faixa:
                continue
            np = carro.posicao
            if p > np:
                continue
            c_intervalo = [np, np + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE]
            bloqueado_p1 = (
                c_intervalo[0] <= intervalo[0] and intervalo[0] <= c_intervalo[1]
            )
            bloqueado_p2 = (
                c_intervalo[0] <= intervalo[1] and intervalo[1] <= c_intervalo[1]
            )
            if bloqueado_p1 or bloqueado_p2:
                return True, carro
        return False, None

    def get_carro_velocidade_baseline(self, carro: Carro):
        # [TODO] Adicionar aceleração do carro
        return carro.velocidade

    def get_next_pista(self, carro: Carro) -> Pista:
        if carro.pista_i == carro.local_destino.pista:
            # [TODO] o carro precisa voltar?
            # [TODO] o carro precisa seguir reto?
            return Pista

        passos = self.grafo_pista.get_passos_dijkstra(
            carro.pista_i, carro.local_destino.pista
        )

        if len(passos) == 1:
            return Pista

        # passo 0 é a pista atual, logo 1 é a próxima
        return self.pistas[passos[1]]

    def clonar_simulacao(self) -> "Simulation":
        return copy.deepcopy(self)

    # Esse função simula um futuro onde todos os carros
    # ficam na mesma faixa onde estão. Ela tenta encontrar
    # o caminho mais rápido para o carro atual chegar até
    # seu destino final.
    # [v1] Não existem interações entre múltiplas faixas.
    def prever_melhor_jogada(self, carro):
        jogadas: tuple[callable[[Carro], bool], callable[[Carro]]] = [
            (self.pode_carro_virar_pra_direita, self.virar_carro_pra_direita),
            (self.pode_carro_virar_pra_esquerda, self.virar_carro_pra_esquerda),
        ]

        for pista in self.get_pistas_acessiveis_por_carro(carro):
            jogadas.append(
                (lambda: True, lambda: self.entrar_carro_em_outra_pista(pista))
            )

        # essa abstração serve pra prever o futuro sem alterar o estado atual
        # e todos os motoristas na pista fazem exatamente isso enquanto dirigem
        simulacao = self.clonar_simulacao()
        for jogadas in jogadas():
            pass

    def virar_carro_pra_direita(self, carro):
        pass

    def virar_carro_pra_esquerda(self, carro):
        pass

    def entrar_carro_em_outra_pista(self, carro):
        # [TODO] Implementar
        return []

    def pode_carro_virar_pra_direita(self, carro) -> bool:
        pass

    def pode_carro_virar_pra_esquerda(self, carro) -> bool:
        pass

    def get_pistas_acessiveis_por_carro(self, carro) -> list[Pista]:
        # [TODO] Implementar
        return []
