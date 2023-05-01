import datetime
import time
import os

# remove print de suporte do pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame.freetype  # Import the freetype module.


from .sim import *
from .geometry import *


class DrawItem:
    def __init__(self):
        pass

    def draw(self, scr: pygame.Surface):
        eprint("draw called on abstract drawitem", cexit=True)

    def draw_polygon(self, scr, cor, rect):
        global RENDER_SCALE
        for item in rect:
            item[0] *= RENDER_SCALE
            item[1] *= RENDER_SCALE

        pygame.draw.polygon(scr, cor, rect)


class Drawer:
    x: int = 0
    draw_items: list[DrawItem]
    draw_items_locked: bool = False

    def __init__(self, draw_items: list[DrawItem] = []):
        self.draw_items = draw_items
        self.draw_items_locked = False

    def draw(self, scr: pygame.Surface, scale: int = 1):
        self.draw_items_locked = True

        scr.fill((255, 255, 255))

        for draw_item in self.draw_items:
            draw_item.draw(scr)

        pygame.display.flip()

        self.draw_items_locked = False

    def set(self, draw_items: list[DrawItem]):
        if self.draw_items_locked:
            raise Exception("Cannot set draw items while drawing")
        self.draw_items = draw_items


class TextDrawer(DrawItem):
    txt: str
    cor: cor
    font: pygame.font

    def __init__(self, txt: str, x: int, y: int, cor: cor = (0, 0, 0)):
        self.txt = txt
        self.x = x
        self.y = y
        self.cor = cor
        self.font = pygame.freetype.SysFont("Verdana", 12)

    def draw(self, scr: pygame.Surface):
        global RENDER_SCALE
        self.font.render_to(
            scr, (self.x * RENDER_SCALE, self.y * RENDER_SCALE), self.txt, cor
        )


class PistaDrawer(DrawItem):
    pista: Pista = None

    n_divisorias: int
    n_faixas: int
    largura: float
    comprimento: float
    l_eixo: int
    c_eixo: int

    def __init__(self, pista: Pista):
        self.pista = pista
        self.n_faixas = len(pista.faixas)
        self.n_divisorias = self.n_faixas - 1

        self.largura = (
            LARGURA_DIVISORIA * self.n_divisorias + LARGURA_FAIXA * self.n_faixas
        )
        self.comprimento = distancia_euclidiana(self.pista.p1, self.pista.p2)

    def draw(self, scr: pygame.Surface):
        last_faixa = None
        dlt = 0.0
        fx = 0
        dv = 0

        for faixa in self.pista.faixas:
            if last_faixa is not None:
                dlt = fx * LARGURA_FAIXA + dv * LARGURA_DIVISORIA
                self.draw_divisoria(dlt, scr, last_faixa, faixa)
                dv += 1

            dlt = fx * LARGURA_FAIXA + dv * LARGURA_DIVISORIA
            self.draw_faixa(dlt, scr, faixa)

            last_faixa = faixa
            fx += 1

        for carro in self.pista.carros:
            self.draw_carro(scr, carro)

    def get_cor_divisoria(self, faixa_anterior: Faixa, faixa_proxima: Faixa) -> cor:
        tipos = enum_list([faixa_anterior.tipo, faixa_proxima.tipo])
        if tipos == ["acostamento", "geral"]:
            return COR_DIVISORIA_FAIXA_ACOSTAMENTO
        elif tipos == ["acostamento", "acostamento"]:
            eprint("acostamento seguido de acostamento")
            exit(1)
        elif faixa_anterior.sentido == faixa_proxima.sentido:
            return COR_DIVISORIA_FAIXA_SENTIDO_IGUAL
        elif faixa_anterior.sentido != faixa_proxima.sentido:
            return COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE
        else:
            eprint(
                "Tipo de faixa irreconhecivel: "
                + str(faixa_anterior.tipo)
                + " "
                + str(faixa_proxima.tipo)
            )
            exit(1)

    def montar_faixa_divisoria_retangulo(
        self, p1: point, p2: point, dlt: float, clargura: float
    ) -> poligno:
        # vetor perpendicular a pista, seu tamanho é metade da largura da pista
        v12 = get_vetor(p1, p2)
        v12 = rotacionar_vetor_horario(v12, rad=math.pi / 2)
        v12 = normalizar_vetor(v12)
        v12 = multiplica_vetor(v12, -self.largura / 2)

        # ponto base do retangulo da pista
        pb = soma_vetor(p1, v12)

        # vetor de deslocamento do ponto mais proximo a pb da faixa ou divisoria em relacao a pista
        vdelta = multiplica_vetor(v12, -1)
        vdelta = normalizar_vetor(vdelta)
        vdelta = multiplica_vetor(vdelta, dlt)

        # vetor de deslocamento da largura da faixa ou divisoria
        vlargura = multiplica_vetor(v12, -1)
        vlargura = normalizar_vetor(vlargura)
        vlargura = multiplica_vetor(vlargura, clargura)

        # pontos do retangulo da faixa ou divisoria, onde ret1 é mais próximo de pb que ret2
        ret1 = soma_vetor(pb, vdelta)
        ret2 = soma_vetor(ret1, vlargura)
        ret3 = soma_vetor(ret1, get_vetor(p1, p2))
        ret4 = soma_vetor(ret2, get_vetor(p1, p2))

        # pontos do retangulo da faixa ou divisoria
        # note como a ordem dos pontos é expressa como um polígno retangular
        return [ret1, ret2, ret4, ret3]

    def montar_carro_retangulo2(self, carro: Carro):
        dlt: float = (
            carro.faixa_i * LARGURA_FAIXA
            + min(carro.faixa_i, 0) * LARGURA_DIVISORIA
            + (LARGURA_FAIXA - LARGURA_CARRO) / 2.0
            + FATOR_AJUSTE_CARRO_VISUAL
        )

        r1, r2, r3, r4 = self.montar_faixa_divisoria_retangulo(
            self.pista.p1, self.pista.p2, dlt, LARGURA_CARRO
        )

        d1 = carro.posicao / self.comprimento  # deve estar em [0,1]
        d2 = (carro.posicao + LARGURA_CARRO) / self.comprimento  # deve estar em [0,1]

        d1y = d1
        d2y = d2

        if self.pista.p1[Y] > self.pista.p2[Y]:
            d1y = 1.0 - d1y
            d2y = 1.0 - d2y

        # ideia seria pegar a média ponderada dos pontos
        # que são calculados no retângulo da faixa
        # baseado na posição (aka. quilometragem) do carro na pista

        x1 = math.fabs(r1[X] - r4[X]) * d1 + min(r1[X], r4[X])
        x2 = math.fabs(r1[X] - r4[X]) * d2 + min(r1[X], r4[X])
        x3 = math.fabs(r2[X] - r3[X]) * d1 + min(r2[X], r3[X])
        x4 = math.fabs(r2[X] - r3[X]) * d2 + min(r2[X], r3[X])

        y1 = math.fabs(r2[Y] - r3[Y]) * d1y + min(r2[Y], r3[Y])
        y2 = math.fabs(r2[Y] - r3[Y]) * d2y + min(r2[Y], r3[Y])
        y3 = math.fabs(r1[Y] - r4[Y]) * d1y + min(r1[Y], r4[Y])
        y4 = math.fabs(r1[Y] - r4[Y]) * d2y + min(r1[Y], r4[Y])

        ret1 = [x1, y1]
        ret2 = [x2, y2]
        ret3 = [x3, y3]
        ret4 = [x4, y4]

        return [ret1, ret2, ret4, ret3]

    def draw_divisoria(
        self,
        dlt: float,
        scr: pygame.Surface,
        faixa_anterior: Faixa,
        faixa_proxima: Faixa,
    ):
        cor = self.get_cor_divisoria(faixa_anterior, faixa_proxima)

        rect = self.montar_faixa_divisoria_retangulo(
            self.pista.p1, self.pista.p2, dlt, LARGURA_DIVISORIA
        )

        self.draw_polygon(scr, cor, rect)

    def draw_faixa(self, dlt: float, scr: pygame.Surface, faixa: Faixa):
        cor = COR_FAIXA
        if faixa.tipo == FaixaTipo["acostamento"]:
            cor = COR_ACOSTAMENTO

        # botar setas pra indicar direção?

        rect = self.montar_faixa_divisoria_retangulo(
            self.pista.p1, self.pista.p2, dlt, LARGURA_FAIXA
        )

        self.draw_polygon(scr, cor, rect)

    def draw_carro(self, scr: pygame.Surface, carro: Carro):
        rect = self.montar_carro_retangulo2(carro)

        if carro.ativado == False:
            self.draw_polygon(scr, COR_CARRO_COMPLETO, rect)
        else:
            self.draw_polygon(scr, carro.cor, rect)


class GUI:
    step_time = None
    last_time = None
    running = False
    drawer = None

    resolution: vetor
    virtual_resolution: vetor
    fullscreen: bool
    render_scale: int
    max_fps: float

    scr: pygame.Surface = None

    pending_update = None

    def __init__(
        self, max_fps=60, resolution=[600, 500], fullscreen=False, render_scale=2
    ):
        pygame.init()
        pygame.display.set_caption("Simulador de trânsito")
        pygame.output = dprint

        self.running = True
        self.max_fps = max_fps
        self.step_time = datetime.timedelta(seconds=1 / self.max_fps)
        self.resolution = resolution
        self.virtual_resolution = multiplica_vetor(resolution, render_scale)
        self.fullscreen = fullscreen
        self.render_scale = render_scale

        self.drawer = Drawer([])
        self.scr = pygame.display.set_mode(tuple(resolution))

        if self.fullscreen:
            pygame.display.toggle_fullscreen()

        global RENDER_SCALE
        RENDER_SCALE = render_scale

    def render(self):
        self.apply_pending_update()

        self.last_time = datetime.datetime.now()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise Exception("user closed program")

        self.drawer.draw(self.scr, scale=self.render_scale)

        if self.last_time is not None:
            diff = datetime.datetime.now() - self.last_time

            if self.step_time > diff:
                wait_time = (self.step_time - diff) / SEC_IN_MICROSECONDS
                time.sleep(wait_time.seconds)

    def exit(self):
        pygame.quit()

    def update(self, pistas: list[Pista]):
        self.pending_update = {"pistas": pistas}

        try:
            draw_items = []
            draw_items += [PistaDrawer(pista) for pista in pistas]
            self.drawer.set(draw_items)
        except Exception as e:
            if self.drawer.draw_items_locked == True:
                return
            else:
                eprint("falha inesperada na atualização de figuras a se desenhar", e)

        self.pending_update = None

    def apply_pending_update(self):
        if self.pending_update is not None:
            self.update(self.pending_update["pistas"])
