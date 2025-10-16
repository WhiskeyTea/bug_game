import pygame
from sys import exit


class Bug(pygame.sprite.Sprite):
    def __init__(self, pos=(600, 600)):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('graphics/bug.png').convert_alpha(), 0, 0.05)
        self.pos = pos
        self.rect = self.image.get_rect(midbottom = pos)

    def move(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)


class Line(pygame.sprite.Sprite):
    def __init__(self, surf, start, end, color='#000000', width=5):
        super().__init__()
        self.start = start
        self.end = end
        self.color = color
        self.width = width
        self.surf = surf

    def draw(self):
        pygame.draw.aaline(self.surf, self.color, self.start, self.end, width=self.width)



pygame.init()
game_state = 1  # ["start", "active"]
screen = pygame.display.set_mode((1280, 720))
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
                line = Line(screen, mouse_pos, st, "#000000")
                line.draw()
                lines.add(line)


    if game_state:
        bug.draw(screen)
        mouse_pos = pygame.mouse.get_rel()
    else:
        test_font = pygame.font.Font(None, 60)  # insert '<folder with font>/<filename.ttf>' instead of None
        text_surface = test_font.render('Hello', True, 'Blue')
        text_rect = text_surface.get_rect(center = (500, 500))
        screen.blit(text_surface, text_rect)


    pygame.display.update()  # shows what was drawn
    clock.tick(60)  # FPS ceiling