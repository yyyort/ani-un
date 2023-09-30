import pygame
from random import randint

# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

class Player(pygame.sprite.Sprite):
    def __init__(self, dt):
        super().__init__()  
        player_f = pygame.image.load("assets/player.png").convert_alpha()
        player_lf = pygame.image.load("assets/player-l.png").convert_alpha()
        self.player_frames = [player_f, player_lf]
        self.player_index = 0
        self.image = self.player_frames[self.player_index]
        self.image = pygame.transform.scale(self.image, (100, 100))
        #self.image = pygame.image.load("assets/player.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom=(width / 2, height - 80))
        self.speed = 1000
        self.dt = dt    


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed * self.dt
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed * self.dt

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_index = 1
            self.image = self.player_frames[self.player_index]
            self.image = pygame.transform.flip(self.image, True, False)
        elif keys[pygame.K_d]:
            self.player_index = 1
            self.image = self.player_frames[self.player_index]
        else:
            self.player_index = 0
            self.image = self.player_frames[self.player_index]
            self.image = pygame.transform.scale(self.image, (100, 100))

    """ def movement(self):
        randomx = randint(0, width)
        self.rect.x = randomx """

    def update(self):
        self.player_input()
        self.animation_state()
        """ self.movement()
 """