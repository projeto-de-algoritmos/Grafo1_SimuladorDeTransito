import json
from enum import Enum
import traceback
import copy

from .geometry import *
from .gui import *
from .const import *
from .algoritmos import *


cor = tuple[int, int, int]

Direcao = Enum("Direcao", "normal contrario")
FaixaTipo = Enum("FaixaTipo", "acostamento geral")


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

    def clonar(self) -> "Carro":
        return copy.deepcopy(self)


# [TODO] Fazer adapter grafo-simulacao?


class Jogada:
    cond: any
    jogada: any
    name: str

    def __init__(self, condicao, jogada, name=""):
        self.cond = condicao
        self.jogada = jogada
        self.name = name

    def atende_condicao(self, simulacao: "Simulation", carro: Carro) -> bool:
        cond = self.cond
        return cond(simulacao, carro)

    def executar(self, simulacao: "Simulation", carro: Carro):
        jogada = self.jogada
        jogada(simulacao, carro)


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

    def clonar(self) -> "Simulation":
        return copy.deepcopy(self)

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

    def update(self, prever_jogada=True):
        for carro in self.carros.values():
            velocidade = self.get_carro_velocidade(carro)

            carro.posicao += velocidade / self.tick_rate

            if carro.posicao > carro.pista.get_comprimento() - COMPRIMENTO_CARRO:
                carro.posicao = 0

            if prever_jogada:
                jogada, passos = self.prever_melhor_jogada(carro)
                if jogada != None:
                    jogada.executar(self, carro)

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

    def get_distancia_destino(self, carro: Carro):
        # [TODO] implementar dijkstra nas pistas
        return int(math.fabs(carro.posicao - carro.local_destino.posicao))

    def is_carro_no_destino(self, carro: Carro):
        return self.get_distancia_destino(carro) == 0

    def get_jogadas(self, carro: Carro):
        jogadas: list[Jogada] = [
            Jogada(
                lambda sim, carro: True,
                lambda sim, carro: sim.seguir_em_frente(carro),
                "seguir em frente",
            ),
            Jogada(
                lambda sim, carro: sim.pode_carro_virar_pra_direita(carro),
                lambda sim, carro: sim.virar_carro_pra_direita(carro),
                "virar pra direita",
            ),
            Jogada(
                lambda sim, carro: sim.pode_carro_virar_pra_esquerda(carro),
                lambda sim, carro: sim.virar_carro_pra_esquerda(carro),
                "virar pra esquerda",
            ),
        ]
        for pista in self.get_pistas_acessiveis_por_carro(carro):
            jogadas.append(
                (lambda: True, lambda: self.entrar_carro_em_outra_pista(pista))
            )
        return jogadas

    # Esse função simula um futuro onde todos os carros
    # ficam na mesma faixa onde estão. Ela tenta encontrar
    # o caminho mais rápido para o carro atual chegar até
    # seu destino final.
    # ela retona a acao imediata pra se realizar, bem como os passos que demorou
    # [v1] Não existem interações entre múltiplas faixas.
    def prever_melhor_jogada(self, carro: Carro, passos=1) -> Jogada:
        # se superamos a quantidade de iteração, retornamos
        if passos > MAX_SIM_ITER_COUNT:
            print("depth exceeded")
            return None, 1e18

        jogadas = self.get_jogadas(carro)

        m_jogada = None
        m_passos = 1e18

        # =============== esse é o BFS mais importante do app ===============
        #
        # vamos testar as possibilidades de jogadas até encontrar a ideal.
        # essa abstração serve pra prever o futuro sem alterar o estado atual
        # todos os motoristas na vida real fazem exatamente isso enquanto dirigem
        for jogada in jogadas:
            if jogada.atende_condicao(self, carro):
                # clona pra evitar conflito de estado (performance altissima)
                n_carro: Carro = carro.clonar()
                n_simulacao: Simulation = self.clonar()

                # executa acao de teste
                jogada.executar(n_simulacao, n_carro)

                n_simulacao.update(prever_jogada=False)

                # se chegou ao destino, encontramos uma solução
                if n_simulacao.is_carro_no_destino(n_carro):
                    return jogada, passos + 1

                # vamos testar as jogadas possíveis a partir daqui
                n_jogada, n_passos = n_simulacao.prever_melhor_jogada(
                    n_carro, passos=passos + 1
                )

                # se essa jogada foi melhor que a anterior, atualiza
                if n_passos < m_passos:
                    m_jogada = n_jogada
                    m_passos = n_passos

        if m_jogada is not None:
            print("returning best jogada =", m_jogada.nome, "passos =", m_passos)
        else:
            print("best jogada not found")
        return m_jogada, m_passos

    def seguir_em_frente(self, carro: Carro):
        # apenas um noop pra interface ficar consistente
        pass

    def virar_carro_pra_direita(self, carro: Carro):
        _, i = self.get_faixa_a_direita(carro)
        carro.faixa_i = i
        carro.faixa = self.pistas[carro.pista_i].faixas[i]

    def virar_carro_pra_esquerda(self, carro: Carro):
        _, i = self.get_faixa_a_esquerda(carro)
        carro.faixa_i = i
        carro.faixa = self.pistas[carro.pista_i].faixas[i]

    def pode_carro_virar_pra_direita(self, carro: Carro) -> bool:
        # existe alguma faixa anterior a atual, se o sentido da faixa é normal?
        # existe alguma faixa posterior a atual, se o sentido da faixa é contrario?
        # essa faixa está indo no mesmo sentido?
        # essa faixa é geral, e não um acostamento?
        cf = carro.faixa_i
        pista = self.pistas[carro.pista_i]
        faixa = pista.faixas[carro.faixa_i]

        faixa_a_direita, _ = self.get_faixa_a_direita(carro)

        if (
            faixa_a_direita is None
            or faixa_a_direita.sentido != faixa.sentido
            or faixa_a_direita.tipo != FaixaTipo["geral"]
        ):
            return False

        return True

    def pode_carro_virar_pra_esquerda(self, carro: Carro) -> bool:
        # existe alguma faixa anterior a atual, se o sentido da faixa é normal?
        # existe alguma faixa posterior a atual, se o sentido da faixa é contrario?
        # essa faixa está indo no mesmo sentido?
        # essa faixa é geral, e não um acostamento?
        pista = self.pistas[carro.pista_i]
        faixa = pista.faixas[carro.faixa_i]

        faixa_a_esquerda, _ = self.get_faixa_a_esquerda(carro)

        if (
            faixa_a_esquerda is None
            or faixa_a_esquerda.sentido != faixa.sentido
            or faixa_a_esquerda.tipo != FaixaTipo["geral"]
        ):
            return False

        return True

    def get_faixa_a_direita(self, carro: Carro):
        cf = carro.faixa_i
        pista = self.pistas[carro.pista_i]
        faixa = pista.faixas[carro.faixa_i]
        faixa_a_direita = None
        index = -1

        if faixa.sentido == Direcao["normal"] and cf > 0:
            faixa_a_direita = pista.faixas[cf - 1]
            index = cf - 1
        elif faixa.sentido == Direcao["contrario"] and cf + 1 < len(pista.faixas):
            faixa_a_direita = pista.faixas[cf + 1]
            index = cf + 1

        return faixa_a_direita, index

    def get_faixa_a_esquerda(self, carro: Carro) -> tuple[Faixa, int]:
        cf = carro.faixa_i
        pista = self.pistas[carro.pista_i]
        faixa = pista.faixas[carro.faixa_i]
        faixa_a_esquerda = None
        index = -1

        if faixa.sentido == Direcao["contrario"] and cf > 0:
            faixa_a_esquerda = pista.faixas[cf - 1]
            index = cf - 1
        elif faixa.sentido == Direcao["normal"] and cf + 1 < len(pista.faixas):
            faixa_a_esquerda = pista.faixas[cf + 1]
            index = cf + 1

        return faixa_a_esquerda, index

    def get_pistas_acessiveis_por_carro(self, carro: Carro) -> list[Pista]:
        # [TODO] Implementar
        return []

    def entrar_carro_em_outra_pista(self, carro: Carro):
        # [TODO] Implementar
        return []
