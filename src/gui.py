import pygame
import datetime
import time

from .sim import *
from .geometry import *

# tempo
SEC_IN_MICROSECONDS = 10e6

# cor
COR_ACOSTAMENTO = (60, 60, 60)
COR_FAIXA = (15, 15, 15)
COR_DIVISORIA_FAIXA_SENTIDO_IGUAL = (200, 200, 200)
COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE = (200, 180, 60)
COR_DIVISORIA_FAIXA_ACOSTAMENTO = (160, 160, 160)

# tamanho
LARGURA_DIVISORIA = 2
LARGURA_FAIXA = 6

SCALE = 1


class DrawItem:
    def __init__(self):
        pass

    def draw(self, scr: pygame.Surface):
        eprint("draw called on abstract drawitem", cexit=True)

    def draw_polygon(self, scr, cor, rect):
        for item in rect:
            item[0] /= SCALE
            item[1] /= SCALE
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

        print("\n")

        for faixa in self.pista.faixas:
            if last_faixa is not None:
                dlt = fx * LARGURA_FAIXA + dv * LARGURA_DIVISORIA
                self.draw_divisoria(dlt, scr, last_faixa, faixa)
                dv += 1

            dlt = fx * LARGURA_FAIXA + dv * LARGURA_DIVISORIA
            self.draw_faixa(dlt, scr, faixa)

            last_faixa = faixa
            fx += 1

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

    def montar_retangulo(
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
        vlargura = normalizar_vetor(v12)
        vlargura = multiplica_vetor(vlargura, clargura)

        # pontos do retangulo da faixa ou divisoria, onde ret1 é mais próximo de pb que ret2
        ret1 = soma_vetor(pb, vdelta)
        ret2 = soma_vetor(ret1, vlargura)
        ret3 = soma_vetor(ret1, get_vetor(p1, p2))
        ret4 = soma_vetor(ret2, get_vetor(p1, p2))

        # pontos do retangulo da faixa ou divisoria
        # note como a ordem dos pontos é expressa como um polígno retangular
        return [ret1, ret2, ret4, ret3]

    def draw_divisoria(
        self,
        dlt: float,
        scr: pygame.Surface,
        faixa_anterior: Faixa,
        faixa_proxima: Faixa,
    ):
        cor = self.get_cor_divisoria(faixa_anterior, faixa_proxima)

        rect = self.montar_retangulo(
            self.pista.p1, self.pista.p2, dlt, LARGURA_DIVISORIA
        )

        dprint("draw divisoria color", cor, rect)
        self.draw_polygon(scr, cor, rect)

    def draw_faixa(self, dlt: float, scr: pygame.Surface, faixa: Faixa):
        cor = COR_FAIXA
        if faixa.tipo == FaixaTipo["acostamento"]:
            cor = COR_ACOSTAMENTO

        # botar setas pra indicar direção?

        rect = self.montar_retangulo(self.pista.p1, self.pista.p2, dlt, LARGURA_FAIXA)

        dprint("draw faixa color", cor, rect)
        self.draw_polygon(scr, cor, rect)

        return dlt


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
        self.running = True
        self.max_fps = max_fps
        self.step_time = datetime.timedelta(seconds=1 / self.max_fps)
        self.resolution = resolution
        self.virtual_resolution = multiplica_vetor(resolution, render_scale)
        self.fullscreen = fullscreen
        self.render_scale = render_scale
        SCALE = self.render_scale

        self.drawer = Drawer([])
        self.scr = pygame.display.set_mode(tuple(resolution))

        if self.fullscreen:
            pygame.display.toggle_fullscreen()

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

    def update(self, pistas: list[Pista], carros: list[Carro]):
        self.pending_update = {"pistas": pistas, "carros": carros}

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
            self.update(self.pending_update["pistas"], self.pending_update["carros"])
