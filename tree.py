import pygame
from random import randint

# pygame setup
pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))

class Tree(pygame.sprite.Sprite):
    def __init__(self, x,y, dt):
        super().__init__()
        tree_n = pygame.image.load("assets/tree/1.png").convert_alpha()
        tree_s = pygame.image.load("assets/tree/2.png").convert_alpha()
        self.tree_frames = [tree_n, tree_s]
        self.tree_index = 0
        self.image = self.tree_frames[self.tree_index]
        self.image = pygame.transform.scale(self.image, (200, height - 100))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.sway_time = randint(1,2)
        self.sway_flag = False
        self.sway_duration = 2
        self.dt = dt
        

    """ 
    methods for adding fruit to the tree 
    """
    """ def add_fruit(self):
        if len(fruit_group) < 3:
            fruit_group.add(Fruit(self.rect.centerx + randint(-100,100) , self.rect.y)) """

    """ 
    method to control the animation state of the tree
    """
    def animation_state(self):
        """ print(self.sway_flag) """
        if self.sway_flag and self.sway_duration > 0:
            self.sway()
            self.sway_duration -= self.dt
        elif self.sway_flag and self.sway_duration <= 0:        
            self.sway_time = randint(1,2)
            self.sway_flag = False
            self.sway_duration = 2

    """ 
    method for flagging when the tree should sway 
    """
    def to_sway(self):
        """ print(self.sway_time) """
        if self.sway_time > 0 and self.sway_flag == False:
            self.sway_time -= self.dt
            self.sway_flag = False
            self.sway_duration = 2
        else:
            self.sway_flag = True

    """ 
    method to animate the tree 
    """
    def sway(self):
        self.tree_index += 0.1
        if self.tree_index >= len(self.tree_frames):
            self.tree_index = 0
        self.image = self.tree_frames[int(self.tree_index)]
        self.image = pygame.transform.scale(self.image, (200, height - 100))
        
    def update(self):
        """ self.add_fruit() """
        self.to_sway()
        self.animation_state()
