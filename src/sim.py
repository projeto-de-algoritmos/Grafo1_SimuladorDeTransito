import json
from enum import Enum
import traceback
import datetime
import copy

from .geometry import *
from .gui import *
from .const import *
from .algoritmos import *

cor = tuple[int, int, int]

Direcao = Enum("Direcao", "normal contrario")
FaixaTipo = Enum("FaixaTipo", "acostamento geral")


def elapsed_ms(time: datetime.datetime):
    return (datetime.datetime.now() - time).total_seconds() * 1000


def dprint(*values: object):
    if DEBUG:
        print("[DEBUG]", *values)


def lprint(*values: object):
    if LOG_ENABLED:
        with open("log.txt", "a") as file:
            print("[LOG]", *values, file=file)


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
    aceleracao: float  # [TODO] usar isso\
    next_jogadas: list["Jogada"]

    # serão alteradas durante a simulação
    pista_i: int
    faixa_i: int
    posicao: float
    pista: Pista
    faixa: Faixa

    ativado: bool = True

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

        self.ativado = True

        self.next_jogadas = []

    def clonar(self) -> "Carro":
        return copy.deepcopy(self)


# [TODO] Fazer adapter grafo-simulacao?


# Pode se tratar uma jogada como uma transformação da simulação.
class Jogada:
    cond: any
    jogada: any
    nome: str
    n_passos: int

    def __init__(self, condicao, jogada, n_passos=1, nome=""):
        self.cond = condicao
        self.jogada = jogada
        self.nome = nome
        self.n_passos = n_passos

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

    tick_rate: float  # 1 / milissegundo
    tick: float  #      milissegundo
    delta_t: float  #   segundo

    grafo_pista: Grafo

    next_jogadas_ignoradas: dict[str, int]  # [nome_do_carro]next_cooldown
    prever_jogada_cooldown: int
    skip_prever_jogada_for_ms: int
    time_init: datetime.datetime
    limite_de_recursao: int

    def __init__(
        self,
        cenario_file,
        tick=DEFAULT_TICK,
        limite_de_recursao=0,
        prever_jogada_cooldown=0,
        skip_prever_jogada_for_ms=0,
    ):
        self.next_jogadas_ignoradas = {}
        self.prever_jogada_cooldown = prever_jogada_cooldown

        self.running = True
        self.skip_prever_jogada_for_ms = skip_prever_jogada_for_ms
        self.time_init = datetime.datetime.now()
        self.limite_de_recursao = limite_de_recursao

        self.tick = tick
        self.tick_rate = 1000 / tick
        self.delta_t = tick / 1e3
        lprint(f"tick={self.tick}, tick_rate={self.tick_rate}, delta_t={self.delta_t}")

        global BFS_I
        BFS_I = 0

        pistas, carros = self.read(cenario_file)

        self.pistas = pistas
        self.carros = carros

    def clonar(self) -> "Simulation":
        return copy.deepcopy(self)

    def get_pistas_and_carros(self):
        return self.pistas

    def read(self, cenario_file):
        data = self.read_and_parse_json_file(cenario_file)

        pistas = []
        carros: dict[str, Carro] = {}

        for i in range(len(data["carros"])):
            carro = data["carros"][i]
            nome = carro["nome"]

            origem = Local(
                carro["origem"]["pista"],
                carro["origem"]["faixa"],
                carro["origem"]["posicao"],
            )

            destino = Local(
                carro["destino"]["pista"],
                carro["destino"]["faixa"],
                carro["destino"]["posicao"],
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

            # isso daqui define o cooldown de previsões de futuro para cada carro
            # fazemos aqui dessa forma para que cada carro tenha seu calculo realizado
            # em um momento diferente. quando o cálculo é pesado, isso remove um gargalo
            # incial na simulação. para entender intuitivamente, altere o valor para 0.
            self.next_jogadas_ignoradas[nome] = int(
                self.prever_jogada_cooldown * i / len(data["carros"])
            )

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

        # self.contruir_grafo_pistas(pistas)

        return pistas, carros

    def contruir_grafo_pistas(self, pistas):
        grafo = Grafo()
        grafo.add_nodes(len(pistas))

        for i in range(len(pistas)):
            for j in range(len(pistas)):
                if i == j:
                    continue

                if (
                    pistas[i].p1 == pistas[j].p1
                    or pistas[i].p1 == pistas[j].p2
                    or pistas[i].p2 == pistas[j].p1
                    or pistas[i].p2 == pistas[j].p2
                ):
                    # [TODO] fazer checagem se edge é possível, como numa pista de
                    # mão única que desemboca em outra, nunca é possível entrar nela,
                    # portanto a aresta não existe
                    grafo.add_edge(i, j)
                    grafo.add_edge(j, i)

    def read_and_parse_json_file(self, path):
        with open(path, "r") as f:
            data = json.load(f)
            return data

    def jump_to_next_tick(self):
        pass

    def update(self, prever_jogada=True):
        for carro in self.carros.values():
            if not carro.ativado:
                continue
            if self.is_carro_no_destino(carro):
                carro.ativado = False
                continue

            velocidade, carro_a_frente = self.get_carro_velocidade(carro)

            aproximacao_maxima = COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE

            carro_alem_da_pista = (
                carro.posicao > carro.pista.get_comprimento() - COMPRIMENTO_CARRO
            )

            if carro_alem_da_pista:
                # [TODO] implentação de update em múltiplas pistas
                # pega as proximas pistas
                # existe alguma pista?
                #  se não: volta na faixa sentido contrário
                #   se não tem: adicionar alguma flag de "stuck"
                #  se sim: quantas?
                #   se 1: vai pra ela
                #   se >:
                #       se tem decisão feita: usa
                #       se não: dijkstra
                #           se não tem caminho: volta na faixa sentido contrário
                #               se tem faixa sentido contrário: volta
                #               se não: adicionar alguma flag de "stuck"
                #           se tem: usa

                carro.posicao = carro.pista.get_comprimento() - COMPRIMENTO_CARRO
            elif carro_a_frente is not None:
                carro.posicao = carro_a_frente.posicao - aproximacao_maxima
            else:
                carro.posicao += velocidade * self.delta_t

            if (
                prever_jogada
                and elapsed_ms(self.time_init) > self.skip_prever_jogada_for_ms
            ):
                carro_bloqueando_movimento, _ = self.is_carro_bloqueando_movimento(
                    carro
                )

                jogadas = carro.next_jogadas
                if len(jogadas) > 0 and jogadas[0].n_passos == 0:
                    jogadas = jogadas[1:]
                    carro.next_jogadas = jogadas

                cooldown = self.next_jogadas_ignoradas[carro.nome]
                tentar_prever_jogada = False

                # sempre recalcula jogada se tiver bloqueado
                if carro_bloqueando_movimento and cooldown == 0:
                    tentar_prever_jogada = True
                    carro.next_jogadas = []

                # caso não tenha plano, faça um plano
                if len(jogadas) == 0:
                    tentar_prever_jogada = True

                if cooldown == 0 and tentar_prever_jogada:
                    lprint("< -------- buscando jogadas...")
                    jogadas, _ = self.prever_melhor_jogada(carro)
                    if len(jogadas) > 0:
                        lprint(f"< -------- jogada encontrada: {jogadas[0].nome}")
                    else:
                        lprint("< -------- falhou em encontrar jogada")

                    # ajusta cooldown
                    self.next_jogadas_ignoradas[
                        carro.nome
                    ] = self.prever_jogada_cooldown
                elif cooldown > 0:
                    self.next_jogadas_ignoradas[carro.nome] -= min(cooldown, 1)

                if len(jogadas) > 0:
                    jogadas[0].executar(self, carro)
                    if jogadas[0].n_passos > 1:
                        jogadas[0].n_passos -= 1
                    else:
                        jogadas = jogadas[1:]
                    carro.next_jogadas = jogadas

    def get_carro_velocidade(self, carro: Carro) -> tuple[float, Carro | None]:
        velocidade_baseline = self.get_carro_velocidade_baseline(carro)

        bloqueado, next_carro = self.is_carro_bloqueando_movimento(carro)
        if not bloqueado:
            return velocidade_baseline, None

        vel, _ = self.get_carro_velocidade(next_carro)
        return vel, next_carro

    def is_carro_bloqueando_movimento(self, c_carro) -> tuple[bool, Carro]:
        # verifique se existe algum carro dentro do espaço de movimento do carro atual
        # o carro atual.
        # O bloqueio é definido por um carro que compartilha a mesma faixa e está
        # em algum lugar entre [0,5] metros da posição do carro atual na faixa.

        carro = self.get_proximo_carro(c_carro)
        if carro is None:
            return False, None

        p = c_carro.posicao
        np = carro.posicao

        if p > np:
            return True, carro

        intervalo = [p, p + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE]
        c_intervalo = [np, np + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE]
        bloqueado_p1 = c_intervalo[0] <= intervalo[0] and intervalo[0] <= c_intervalo[1]
        bloqueado_p2 = c_intervalo[0] <= intervalo[1] and intervalo[1] <= c_intervalo[1]

        if bloqueado_p1 or bloqueado_p2:
            return True, carro

        return False, None

    def is_segmento_faixa_ocupado(
        self, seg: tuple[float, float], pista_i: int, faixa_i: int
    ):
        p1, p2 = seg
        for carro in self.carros.values():
            if carro.pista_i == pista_i and carro.faixa_i == faixa_i:
                c1, c2 = (
                    carro.posicao,
                    carro.posicao + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE,
                )
                if (p1 <= c1 <= p2) or (p1 <= c2 <= p2):
                    return True
        return False

    def get_proximo_carro(self, carro: Carro) -> Carro:
        ret = None
        for ccarro in self.carros.values():
            if ccarro.pista_i == carro.pista_i and ccarro.faixa_i == carro.faixa_i:
                if ccarro.posicao > carro.posicao:
                    if ret is None or ret.posicao > ccarro.posicao:
                        ret = ccarro
        return ret

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
        # o ajuste tem o simples propósito de dar uma penalidade para
        # o carro mudar de faixa ou de pista, pequena porém não nula
        ajuste = 0
        if carro.pista_i != carro.local_destino.pista:
            ajuste += 2
        if carro.faixa_i != carro.local_destino.faixa:
            ajuste += 1
        return int(math.fabs(carro.posicao - carro.local_destino.posicao)) + ajuste

    def is_carro_no_destino(self, carro: Carro):
        if carro.pista_i != carro.local_destino.pista:
            return False
        if carro.faixa_i != carro.local_destino.faixa:
            return False
        return self.get_distancia_destino(carro) < FATOR_ARRENDONDAMENTO

    def get_jogadas(self, carro: Carro):
        jogadas: list[Jogada] = [
            Jogada(
                lambda sim, carro: sim.pode_carro_virar_pra_direita(carro),
                lambda sim, carro: sim.virar_carro_pra_direita(carro),
                nome="virar pra direita",
                n_passos=1,
            ),
            Jogada(
                lambda sim, carro: sim.pode_carro_virar_pra_esquerda(carro),
                lambda sim, carro: sim.virar_carro_pra_esquerda(carro),
                nome="virar pra esquerda",
                n_passos=1,
            ),
            Jogada(
                lambda sim, carro: True,
                lambda sim, carro: sim.seguir_em_frente(carro),
                nome="seguir em frente",
                n_passos=0,
            ),
        ]
        for pista in self.get_pistas_acessiveis_por_carro(carro):
            jogadas.append(
                (lambda: True, lambda: self.entrar_carro_em_outra_pista(pista))
            )
        return jogadas

    # Esse função simula um futuro onde todos os carros ficam na mesma faixa onde estão.
    # Ela tenta encontrar o caminho mais rápido para o carro atual chegar até seu destino
    # final. Ela retona a acao imediata pra se realizar, bem como os passos que demorou
    def prever_melhor_jogada(
        self, carro: Carro, passos=0, iter=1
    ) -> tuple[list[Jogada], int]:
        global BFS_I
        BFS_I += 1
        id = BFS_I

        # se superamos a quantidade de iteração, retornamos
        if iter > self.limite_de_recursao:
            lprint(f"(id: {id}) atingiu limite de recursão")
            return [], 1e18

        lprint(
            f"====== prever_melhor_jogada (id: {id}) nome={carro.nome} pos={carro.posicao} passos={passos} iter={iter}"
        )

        if self.is_carro_no_destino(carro):
            return [], passos

        melhores_jogadas = []
        jogadas = self.get_jogadas(carro)
        m_passos = 1e18

        # =============== esse é o DFS mais importante do app ===============
        #
        # vamos testar as possibilidades de jogadas até encontrar a ideal.
        # essa abstração serve pra prever o futuro sem alterar o estado atual
        # todos os motoristas na vida real fazem exatamente isso enquanto dirigem

        for jogada in jogadas:
            jogada = self.amortizar_calculo(jogada, carro)

            if jogada.atende_condicao(self, carro):
                # clona pra evitar conflito de estado (performance altissima)
                lprint(f"atende condicao (id: {id})", jogada.nome)
                n_simulacao: Simulation = self.clonar()
                n_carro: Carro = n_simulacao.carros[carro.nome].clonar()

                # executa acao de teste
                lprint(f"executa mudanca (id: {id}) jogada='{jogada.nome}'")
                jogada.executar(n_simulacao, n_carro)
                n_passos = passos + jogada.n_passos
                passos += jogada.n_passos

                lprint(
                    f"simulando futuro (id: {id}) jogada='{jogada.nome}' n_passos={n_passos}"
                )
                for i in range(0, jogada.n_passos):
                    n_simulacao.update(prever_jogada=False)

                lprint(
                    f"(id: {id}) carro_no_destino={n_simulacao.is_carro_no_destino(n_simulacao.carros[carro.nome])} posicao={n_carro.posicao}, faixa={n_carro.faixa_i}, destino={n_carro.local_destino.posicao}, distancia={n_simulacao.get_distancia_destino(n_simulacao.carros[carro.nome])}"
                )

                # se chegou ao destino, encontramos uma solução
                if n_simulacao.is_carro_no_destino(n_simulacao.carros[carro.nome]):
                    # self.apply_update_state(sts)
                    lprint(f"(id: {id}) ret solucao")
                    return [jogada], passos + 1

                # vamos testar as jogadas possíveis a partir daqui
                n_jogadas, n_passos = n_simulacao.prever_melhor_jogada(
                    n_carro, passos=n_passos, iter=iter + 1
                )

                # se essa jogada foi melhor que a anterior, atualiza
                if n_passos < m_passos:
                    melhores_jogadas += [jogada] + n_jogadas
                    m_passos = n_passos
                    lprint(
                        f"nova melhor jogada (id: {id}) jogada='{jogada.nome}' n_passos={n_passos} iter={iter} carro={carro.nome} "
                    )

                passos -= jogada.n_passos

                # self.apply_update_state(sts)

        if len(melhores_jogadas) > 0:
            lprint(
                f"(id: {id}) ret {carro.nome} {iter} {m_passos} {melhores_jogadas[0].nome}"
            )
        else:
            lprint(f"(id: {id}) ret none")
        return melhores_jogadas, m_passos

    def amortizar_calculo(self, jogada: Jogada, carro: Carro, depth=1) -> Jogada:
        # como todos os carros a partir do momento que estou calculando não irão mudar de faixa
        # posso combinar numa única decisão todos os passos até que o carro
        # - siga até a posição do proximo carro na pista
        # - siga até o final da pista
        # - ou se essa pista é contém seu destino final, siga até o destino final
        # com isso irei somar um numero de passos igual ao tick rate da simulação como se fossem
        # decisões de seguir reto. ou seja, muitos calculos desnecessários serão evitados

        if jogada.nome != "seguir em frente":
            return jogada
        n_passos = jogada.n_passos
        vel = self.get_carro_velocidade_baseline(carro)
        dist = 1e18
        found = False
        p = carro.posicao

        bloqueado, nxt_carro = self.is_carro_bloqueando_movimento(carro)
        if nxt_carro is not None:
            if bloqueado:
                # segue atrás do carro
                if depth > 0:
                    n_jogada = copy.deepcopy(jogada)
                    n_jogada = self.amortizar_calculo(n_jogada, nxt_carro, depth - 1)
                    return n_jogada
            else:
                # segue até o proximo carro?
                dist = min(nxt_carro.posicao - p, dist)
                found = True

        if carro.local_destino.pista == carro.pista_i:
            # segue até o destino final?
            found = True
            dist = min(carro.local_destino.posicao - p, dist)
        else:
            # segue até o final da pista?
            found = True
            dist = min(self.pistas[carro.pista_i].get_comprimento() - p, dist)

        if not found or dist <= self.delta_t * vel:
            return jogada

        n_passos = math.floor(dist / (vel * self.delta_t))
        lprint(
            f"amorizar_calculo dist={n_passos * self.delta_t * vel} pos={carro.posicao} pos_after={carro.posicao + n_passos * self.delta_t * vel + carro.posicao}"
        )
        jogada.n_passos = n_passos
        return jogada

    def seguir_em_frente(self, carro: Carro):
        # apenas um noop pra interface ficar consistente
        pass

    def virar_carro_pra_direita(self, carro: Carro):
        _, i = self.get_faixa_a_direita(carro)
        carro.faixa_i = i
        carro.faixa = self.pistas[carro.pista_i].faixas[i]
        self.carros[carro.nome] = carro

    def virar_carro_pra_esquerda(self, carro: Carro):
        _, i = self.get_faixa_a_esquerda(carro)
        carro.faixa_i = i
        carro.faixa = self.pistas[carro.pista_i].faixas[i]
        self.carros[carro.nome] = carro

    def pode_carro_virar_pra_direita(self, carro: Carro) -> bool:
        # existe alguma faixa anterior a atual, se o sentido da faixa é normal?
        # existe alguma faixa posterior a atual, se o sentido da faixa é contrario?
        # essa faixa está indo no mesmo sentido?
        # essa faixa é geral, e não um acostamento?
        cf = carro.faixa_i
        pista = self.pistas[carro.pista_i]
        faixa = pista.faixas[carro.faixa_i]

        faixa_a_direita, faixa_direita_i = self.get_faixa_a_direita(carro)

        if (
            faixa_a_direita is None
            or faixa_a_direita.sentido != faixa.sentido
            or faixa_a_direita.tipo != FaixaTipo["geral"]
        ):
            return False

        if self.is_segmento_faixa_ocupado(
            (
                carro.posicao,
                carro.posicao + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE,
            ),
            carro.pista_i,
            faixa_direita_i,
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

        faixa_a_esquerda, faixa_esquerda_i = self.get_faixa_a_esquerda(carro)

        if (
            faixa_a_esquerda is None
            or faixa_a_esquerda.sentido != faixa.sentido
            or faixa_a_esquerda.tipo != FaixaTipo["geral"]
        ):
            return False

        if self.is_segmento_faixa_ocupado(
            (
                carro.posicao,
                carro.posicao + COMPRIMENTO_CARRO + DISTANCIA_MINIMA_CARRO_A_FRENTE,
            ),
            carro.pista_i,
            faixa_esquerda_i,
        ):
            return False

        return True

    def get_faixa_a_esquerda(self, carro: Carro):
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

    def get_faixa_a_direita(self, carro: Carro) -> tuple[Faixa, int]:
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
