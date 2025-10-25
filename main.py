import pygame
from sys import exit
import numpy as np
import math
from random import choice

class Bug(pygame.sprite.Sprite):
    def __init__(self, pos=np.array([600, 600]), speed=1, angle=-math.pi / 2):
        super().__init__()
        self.angle = angle
        self.original_image = pygame.image.load('graphics/bug.png').convert_alpha()
        self.pos = pos
        self.image = self.image = pygame.transform.rotozoom(self.original_image, -math.degrees(self.angle), 1)
        self.rect = self.image.get_frect(center = pos)
        self.speed = speed
        self.vec = np.array([math.cos(self.angle) * speed, math.sin(self.angle) * speed])
        self.mask = pygame.mask.from_surface(self.image)

    def change_dir(self, a=0.1):
        self.angle += a
        self.vec = np.array([math.cos(self.angle), math.sin(self.angle)]) * self.speed
        self.update_image()

    def update_image(self):
        self.image = pygame.transform.rotozoom(self.original_image, -math.degrees(self.angle), 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, k=1):
        self.rect.center += self.vec * k

    def check_future_collision(self, time=20):
        future_rect = self.rect.copy()
        future_rect.center += self.vec * time
        for l in lines:
            offset = (int(l.rect.left - future_rect.left),
                      int(l.rect.top - future_rect.top))
            if self.mask.overlap(l.mask, offset):
                self.change_dir()

    def update(self):
        self.check_future_collision()
        self.move()




class Line(pygame.sprite.Sprite):
    def __init__(self, start, end, color='#000000', width=5):
        super().__init__()
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(self.surf, self.color, self.start, self.end, width=self.width)
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect()

    def draw(self):
        screen.blit(self.surf, (0, 0))



def crd_sum(x, y):
    return x[0] + y[0], x[1] + y[1]


def check_future_collision(time):
    return pygame.sprite.spritecollide(Bug(bug.sprite.pos + bug.sprite.vec * time), lines, False)



pygame.init()
game_state = 1  # ["start", "active"]
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill("gray")
pygame.display.set_caption("Букашка")
clock = pygame.time.Clock()

bug = pygame.sprite.GroupSingle()
bug.add(Bug())
lines = pygame.sprite.Group()
last_pos = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state:

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_SPACE]:
                mouse_pos = pygame.mouse.get_pos()
                mv = pygame.mouse.get_rel()
                st = tuple(mouse_pos[i] - mv[i] for i in [0, 1])
                line = Line(st, mouse_pos, "#000000")
                lines.add(line)


    if game_state:
        screen.blit(bg, (0, 0))
        bug.draw(screen)
        bug.update()
        for l in lines:
            l.draw()
        lines.update()
        mouse_pos = pygame.mouse.get_rel()
    else:
        test_font = pygame.font.Font(None, 60)  # insert '<folder with font>/<filename.ttf>' instead of None
        text_surface = test_font.render('Hello', True, 'Blue')
        text_rect = text_surface.get_rect(center = (500, 500))
        screen.blit(text_surface, text_rect)


    pygame.display.update()  # shows what was drawn
    clock.tick(60)  # FPS ceiling