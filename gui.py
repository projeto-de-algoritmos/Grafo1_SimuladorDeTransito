import pygame
import datetime
import time


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
        pass

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

point = list[int, int]
direcao = str["leste", "oeste", "norte", "sul"]

def Pista(DrawItem):
    x, y, w, h: int
    direcao: str
    color = (0, 0, 0)

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __init__(self, p1: point, p2: point):
        self.x = p1[0]
        self.y = p1[1]
        self.w = p2[0] - p1[0]
        self.h = p2[1] - p1[1]

    def draw(self, scr: pygame.Surface):
        pygame.draw.rect(scr, self.color, (self.x, self.y, self.w, self.h))

        if 

        for i in range(self.x, self.x + self.w, 10):
            pygame.draw.line(scr, self.color, (i, self.y), (i, self.y + self.h))
        pygame.draw.rect(scr, self.color, (self.x, self.y, self.w, self.h))

if __name__ == '__main__':
    gui = GUI()
    gui.init()
    gui.run()
