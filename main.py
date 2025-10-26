import pygame
from sys import exit
import numpy as np
import math

class Bug(pygame.sprite.Sprite):
    def __init__(self, pos=np.array([600, 600]), speed=1.5, angle=-math.pi / 2):
        super().__init__()
        self.angle = angle
        self.original_image = pygame.image.load('graphics/bug.png').convert_alpha()
        self.pos = pos
        self.image = pygame.transform.rotozoom(self.original_image, -math.degrees(self.angle), 1)
        self.rect = self.image.get_frect(center = pos)
        self.speed = speed
        self.vec = np.array([math.cos(self.angle), math.sin(self.angle)]) * self.speed
        self.mask = pygame.mask.from_surface(self.image)

    def change_dir(self, a=0.1):
        self.angle += a
        self.vec = np.array([math.cos(self.angle), math.sin(self.angle)]) * self.speed
        self.update_image()

    def update_image(self):
        self.image = pygame.transform.rotozoom(self.original_image, -math.degrees(self.angle), 1)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.center += self.vec

    def check_future_collision(self, time=20):
        future_rect = self.rect.copy()
        future_rect.center += self.vec * time
        flag = False
        for l in lines:
            offset = np.array(l.rect.topleft) - np.array(future_rect.topleft)
            if self.mask.overlap(l.mask, offset):
                flag = True
                break
        if flag:
            collisions = []
            for future_angle in math.pi / 8, -math.pi / 8:
                future_rect = self.rect.copy()
                future_vec = np.array([math.cos(self.angle + future_angle), math.sin(self.angle + future_angle)]) * self.speed
                future_rect.center += future_vec * time
                cnt = 0
                for l in lines:
                    offset = np.array(l.rect.topleft) - np.array(future_rect.topleft)
                    if self.mask.overlap(l.mask, offset):
                        cnt += 1
                collisions.append(cnt)
            print(collisions)
            if collisions[0] < collisions[1]:
                self.change_dir(math.pi / 20)
            else:
                self.change_dir(-math.pi / 20)

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
        # self.surf = pygame.Surface(abs(start - end) + 5, pygame.SRCALPHA)
        # bg.blit(self.surf, (min(start[0] - 5, end[0] - 5), min(start[1] - 5, end[1] - 5)))
        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.aaline(self.surf, self.color, self.start, self.end, width=self.width)
        # print(self.rect.topleft, self.rect.bottomright, start, end, self.surf.get_size())
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect()

    def draw(self):
        screen.blit(self.surf, (0, 0))


pygame.init()
game_state = 1  # ["start", "active"]
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = '#646464'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg.fill(BG_COLOR)
pygame.display.set_caption("Букашка")
clock = pygame.time.Clock()

bug = pygame.sprite.GroupSingle()
bug.add(Bug())
lines = pygame.sprite.Group()
top_side = Line((0, 0), (SCREEN_WIDTH - 0, 0), color=BG_COLOR, width=1)
bottom_side = Line((0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), color=BG_COLOR, width=1)
left_side = Line((0, 0), (0, SCREEN_HEIGHT), color=BG_COLOR, width=1)
right_side = Line((SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), color=BG_COLOR, width=1)
lines.add(left_side)
lines.add(right_side)
lines.add(top_side)
lines.add(bottom_side)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state:

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_SPACE]:
                mouse_pos = np.array(pygame.mouse.get_pos())
                mv = np.array(pygame.mouse.get_rel())
                st = mouse_pos - mv
                line = Line(st, mouse_pos, "#000000")
                lines.add(line)


    if game_state:
        screen.blit(bg, (0, 0))
        bug.draw(screen)
        bug.update()
        for l in lines:
            l.draw()
        mouse_pos = pygame.mouse.get_rel()
    else:
        test_font = pygame.font.Font(None, 60)  # should insert '<folder with font>/<filename.ttf>' instead of None later
        text_surface = test_font.render('Hello', True, 'Blue')
        text_rect = text_surface.get_rect(center = (500, 500))
        screen.blit(text_surface, text_rect)


    pygame.display.update()
    clock.tick(60)