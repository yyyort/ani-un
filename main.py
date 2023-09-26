# Example file showing a circle moving on screen
import pygame
from random import randint

#constants
width = 1280
height = 720

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom=(width / 2, height - 80))
        self.speed = 500

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed * dt
    
    def update(self):
        self.player_input()

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom=(randint(0, width), height / 4))
        self.speed = 200
        self.fallTime = randint(1, 5)

    def gravity(self):
        if self.fallTime > 0:
            self.fallTime -= dt
        else:
            self.rect.y += self.speed * dt
    
    def update(self):
        self.gravity()
        self.destroy()

    def destroy(self):
        if self.rect.y > height - 200:
            self.kill()

#collision
def collision():
    if pygame.sprite.spritecollide(player.sprite, fruit_group, True):
        print("collide")


# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

sky = pygame.image.load("assets/Sky.png").convert()
ground = pygame.image.load("assets/ground.png").convert()

skyScaled = pygame.transform.scale(sky, (width, height))
groundScaled = pygame.transform.scale(ground, (width, 100))

#class setup
player = pygame.sprite.GroupSingle()
player.add(Player())

fruit_group = pygame.sprite.Group()

""" fruit = pygame.sprite.Group()
for i in range(randint(1, 10)):
    fruit.add(Fruit()) """

# timer
fruit_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fruit_timer, 1000)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == fruit_timer:
            fruit_group.add(Fruit())

    # draw background
    screen.blit(skyScaled, (0, 0))
    screen.blit(groundScaled, (0, height - 100))
    player.draw(screen)
    player.update()

    
    """ fruit.draw(screen)
    fruit.update() """

    #fruit init
    fruit_group.draw(screen)
    fruit_group.update()

    collision()
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()