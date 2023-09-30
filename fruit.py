import pygame
from random import randint
from util import decrement_health

# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, fallTime, dt):
        super().__init__()
        fruits = [
            'assets/fruits/1.png',
            'assets/fruits/2.png',
            'assets/fruits/3.png',
            'assets/fruits/4.png',
            'assets/fruits/5.png',
            'assets/fruits/6.png',
            'assets/fruits/7.png'
        ]
        self.scale = 0.5
        self.image = pygame.image.load(fruits[randint(0, 6)]).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.rect = self.image.get_rect(midbottom=(randint(x - 10, x + 10), height / 4))
        self.speed = 50
        self.fallTime = fallTime
        """ self.fallTime = randint(1,3) """
        self.angle = 0
        self.dt = dt

    """ 
    methods for animating the fruit fall
    """
    def gravity(self):
        if self.fallTime > 0:
            self.fallTime -= self.dt 
        else:
            self.rect.y += self.speed * 0.1

    """ 
    fruit animation 
    """
    """ def spawn_animation(self):
        if self.scale <= 0.5:
            self.scale += 0.01
            self.image = pygame.transform.scale_by(self.image, self.scale)
        else:
            return False


    def falling_animation(self):
        if self.spawn_animation == False:
            self.angle += 0 * dt
            self.image = pygame.transform.rotate(self.image, self.angle) """
    
    def destroy(self):
        if self.rect.y > height - 100:
            decrement_health()
            self.kill()

    def update(self):
        #self.spawn_animation()
        self.gravity()
        self.destroy()
