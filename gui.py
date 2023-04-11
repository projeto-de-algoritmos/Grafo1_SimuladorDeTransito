import pygame
import datetime
import time
import json
from math import min, max

point = list[int, int]
direcao = str["leste", "oeste", "norte", "sul", "parado"]
faixa_tipo = str["acostamento", "geral"]

cor = tuple(int, int, int)

COR_ACOSTAMENTO = (30, 30, 30)
COR_FAIXA = (15, 15, 15)
COR_DIVISORIA_FAIXA_SENTIDO_IGUAL = (200, 200, 200)
COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE = (200, 200, 0)
COR_DIVISORIA_FAIXA_ACOSTAMENTO = (160, 160, 160)

LARGURA_DIVISORIA = 2


class GUI():
    MAX_FPS = 60
    SEC_IN_MICROSECONDS = 10e6
    STEP_TIME = SEC_IN_MICROSECONDS / MAX_FPS

    scr: pygame.Surface = None
    running = False
    drawer = None

    def __init__(self):
        pass

    def init(self):
        pygame.init()
        self.scr = pygame.display.set_mode((600, 500))
        self.running = True
        self.drawer = Drawer()

    def run(self):
        while self.running:
            ti = datetime.datetime.now()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.drawer.draw(self.scr)

            diff = datetime.datetime.now() - ti
            diff = diff.microseconds

            if self.STEP_TIME > diff:
                wait_time = (self.STEP_TIME - diff) / self.SEC_IN_MICROSECONDS
                time.sleep(wait_time)

    def exit():
        pygame.quit()


class DrawItem():
    def __init__(self):
        pass

    def draw(self, scr: pygame.Surface):
        print("FAILED TO IMPLEMENT DRAW")
        exit(1)


class Drawer():
    x: int = 0
    draw_items: list[DrawItem]

    def __init__(self):
        pass

    def draw(self, scr: pygame.Surface):
        scr.fill((255, 255, 255))

        pygame.draw.circle(scr, (200, 0, 0), (self.x, 250), 80)
        pygame.display.flip()

        self.x = self.x + 1

        if self.x > 600-250:
            self.x = 250/2.0


class Faixa():
    tipo: faixa_tipo
    direcao_de_movimento: direcao
    sentido: direcao

    def __init__(self, name, relativo, sentido):
        self.name = name
        self.relativo = relativo
        self.sentido = sentido


class Pista():
    p1: point
    p2: point
    direcao: direcao
    faixas: list[Faixa]
    step_w: int = None

    def __init__(self, p1: point, p2: point, direcao: direcao, faixas: list[Faixa]):
        self.p1 = p1
        self.p2 = p2
        self.direcao = direcao
        self.faixas = faixas


def rect(p1: point, p2: point):
    x = min(p1[0], p2[0])
    y = min(p1[1], p2[1])
    w = max(p1[0], p2[0]) - x
    h = max(p1[1], p2[1]) - y
    return (x, y, w, h)


def get_params_directional_rect(p1: point, p2: point, direcao: direcao, dlt: float):
    x, y, w, h: float

    if direcao == "leste" or direcao == "oeste":
        x, y, w, h = rect(
            [p1[0], p1[1] + dlt], [p2[0], p2[1] + dlt]
        )
    else:
        x, y, w, h = rect(
            [p1[0] + dlt, p1[1]], [p2[0] + dlt, p2[1]]
        )

    return (x, y, w, h)


class FaixaDrawer(DrawItem):
    faixa: Faixa = None

    def __init__(self, faixa: Faixa):
        self.faixa = faixa

    def draw(self, dlt: float, scr: pygame.Surface, p1, p2, direcao: direcao) -> float:
        faixa = self.faixa

        cor = COR_FAIXA
        if self.tipo == "acostamento":
            cor = COR_ACOSTAMENTO

        # botar setas pra indicar direção?

        rect = get_params_directional_rect(p1, p2, direcao, dlt)

        pygame.draw.rect(scr, cor, rect)


class PistaDrawer(DrawItem):
    pista: Pista = None

    def __init__(self, pista: Pista):
        self.pista = pista

    def draw(self, scr: pygame.Surface):
        last_faixa = None
        dlt = 0
        for faixa in self.faixas:
            if last_faixa is not None:
                dlt = dlt + \
                    self.draw_divisoria(
                        dlt, scr, last_faixa, faixa, self.direcao)

            faixa_drawer = FaixaDrawer(faixa)
            dlt = dlt + faixa_drawer.draw(scr)

            last_faixa = faixa

    def get_cor_divisoria(faixa_anterior: Faixa, faixa_proxima: Faixa) -> cor:
        if faixa_anterior.tipo != "acostamento" and faixa_proxima.tipo == "acostamento":
            return COR_DIVISORIA_FAIXA_ACOSTAMENTO
        elif faixa_anterior.tipo == "acostamento" and faixa_proxima.tipo == "acostamento":
            return COR_DIVISORIA_FAIXA_ACOSTAMENTO
        elif faixa_anterior.tipo == "acostamento" and faixa_proxima.tipo == "acostamento":
            print("ERRO: não pode ter acostamento seguido de acostamento")
            exit(1)
        elif faixa_anterior.tipo == faixa_proxima.tipo:
            return COR_DIVISORIA_FAIXA_SENTIDO_IGUAL
        elif faixa_anterior.direcao_de_movimento != faixa_anterior.direcao_de_movimento:
            return COR_DIVISORIA_FAIXA_SENTIDO_DIFERENTE
        else:
            print("ERRO: Tipo de faixa irreconhecivel " +
                  str(faixa_anterior.tipo) + " " + str(faixa_proxima.tipo))
            exit(1)

    def draw_divisoria(self,  dlt: float, scr: pygame.Surface, faixa_anterior: Faixa, faixa_proxima: Faixa, direcao: direcao) -> float:
        cor = self.get_cor_divisoria(faixa_anterior, faixa_proxima)

        dlt = dlt + LARGURA_DIVISORIA
        rect = get_params_directional_rect(
            faixa_anterior.p1, faixa_anterior.p2, direcao, dlt)

        pygame.draw.rect(scr, cor, rect)

        return dlt


def read_and_parse_json_file(path="config.json"):
    with open(path, "r") as f:
        data = json.load(f)
        return data


def execute():
    data = read_and_parse_json_file()

    pistas = []

    for pista in data["pistas"]:
        faixas = []
        for faixa in pista["faixas"]:
            faixa_obj = Faixa(faixa["tipo"], faixa["relativo"], faixa["sentido"])
            faixas.append(faixa_obj)

        pista = Pista(
            p1=pista["p1"],
            p2=pista["p2"],
            direcao=pista["direcao"],
            faixas=faixas
        )

        pistas.append(pista)
    
    gui = GUI()

    gui.drawer.add_draw_item(PistaDrawer(pista))

    gui.init()
    gui.run()


if __name__ == '__main__':
    execute()
