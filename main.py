import pygame
from sys import exit
import numpy as np
import math
# pos=np.array([600, 600]), vec=np.array([0, 0])

class Bug(pygame.sprite.Sprite):
    def __init__(self, pos=np.array([600, 600]), speed=1, angle=0):
        super().__init__()
        self.angle = angle
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/bug.png').convert_alpha(), math.degrees(self.angle), 0.05)
        self.pos = pos
        self.rect = self.image.get_frect(center = pos)
        self.speed = speed
        self.vec = np.array([math.cos(self.angle) * speed, math.sin(self.angle) * speed])

    def change_dir(self):
        self.angle += 0.1
        # self.image = pygame.transform.rotozoom(self.image, math.degrees(self.angle), 1)
        self.vec = np.array([math.cos(self.angle) * self.speed, math.sin(self.angle) * self.speed])

    def move(self, k=1):
        self.rect.center += self.vec * k

    def check_future_collision(self, time=10):
        while pygame.sprite.spritecollide(Bug(self.rect.center + self.vec * time, self.speed, self.angle), lines, False):
            self.change_dir()

    def update(self):
        self.check_future_collision()
        self.move()




class Line(pygame.sprite.Sprite):
    def __init__(self, surf, start, end, color='#000000', width=5):
        super().__init__()
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.surf = surf

    def draw(self):
        self.rect = pygame.draw.aaline(self.surf, self.color, self.start, self.end, width=self.width)


def crd_sum(x, y):
    return x[0] + y[0], x[1] + y[1]


def check_future_collision(time):
    return pygame.sprite.spritecollide(Bug(bug.sprite.pos + bug.sprite.vec * time), lines, False)



pygame.init()
game_state = 1  # ["start", "active"]
screen = pygame.display.set_mode((1280, 720))
screen.fill("gray")
bg = pygame.transform.scale_by(pygame.image.load('graphics/923c508dac22439e4f56502f7181e040.jpg').convert(), 3)
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
                line = Line(bg, mouse_pos, st, "#000000")
                line.draw()
                lines.add(line)


    if game_state:
        screen.blit(bg, (0, 0))
        bug.draw(screen)
        bug.update()
        mouse_pos = pygame.mouse.get_rel()
    else:
        test_font = pygame.font.Font(None, 60)  # insert '<folder with font>/<filename.ttf>' instead of None
        text_surface = test_font.render('Hello', True, 'Blue')
        text_rect = text_surface.get_rect(center = (500, 500))
        screen.blit(text_surface, text_rect)


    pygame.display.update()  # shows what was drawn
    clock.tick(60)  # FPS ceiling