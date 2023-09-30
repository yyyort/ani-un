# Example file showing a circle moving on screen
import pygame
from random import randint, choice
from util import *
from player import *
from fruit import *
from tree import *


# pygame setup
width = 1280
height = 720
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
fps = 60
dt = 0
game_active = False
game_over = False

#constants
score = 0
health = 3
level = 0

pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load("assets/Sky.png").convert()
ground = pygame.image.load("assets/ground.png").convert()


skyScaled = pygame.transform.scale(sky, (width, height))
groundScaled = pygame.transform.scale(ground, (width, 100))


"""
intro
"""

#class setup
player = pygame.sprite.GroupSingle()
player.add(Player(dt=dt))

fruit_group = pygame.sprite.Group()

#tree setup
tree_list = [
    (100, height - 50, dt),
    (300, height - 50, dt),
    (width/2, height - 50, dt),
    (width - 300, height - 50, dt),
    (width - 100, height - 50, dt),
]

trees = pygame.sprite.Group()
for tree in tree_list:
    trees.add(Tree(tree[0], tree[1], tree[2]))

""" 
user events
"""
# timer
fruit_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fruit_timer, 2000)

#time
time_test = pygame.time.get_ticks()
counter = 0
timer = 0

#levels
fruit_spawn = 2
fruit_fall_speed = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        """ 
        spawn randomly
        """    
        """ if event.type == fruit_timer and len(fruit_group) < fruit_spawn:
            fruit_group.add(Fruit(x = randint(0, width), y = height / 4)) """

        """ 
        uncomment if fruit spawn is in the tree 
        """
        """ if event.type == fruit_timer and len(fruit_group) < fruit_spawn:
            fruit_group.add(choice([Fruit(x=tree1[0], y=tree1[1]),
                                    Fruit(x=tree2[0], y=tree2[1]), 
                                    Fruit(x=tree3[0], y=tree3[1])])) """
        if event.type == fruit_timer and len(fruit_group) < fruit_spawn:
            fruit_group.add(choice([Fruit(x=tree.rect.centerx, y=100, fallTime=tree.sway_time, dt=tree.dt) for tree in trees]))
     
            
    if game_active:
        tick = pygame.time.get_ticks()
        if tick - time_test >= 1000:
            timer += 1
            counter += 1
            time_test = tick
        
        if counter >= 60:
            level += 1
            fruit_spawn += 1
            counter = 0

        start_time = int(pygame.time.get_ticks() / 1000)

        # draw background
        screen.blit(skyScaled, (0, 0))
        screen.blit(groundScaled, (0, height - 100))

        trees.draw(screen)
        trees.update()

        #fruit init
        fruit_group.draw(screen)
        fruit_group.update()
        
        if collision(player=player, fruit_group=fruit_group):
            score += 1

        display_score(score)
        display_health()
        display_level(level)
        display_time(counter=counter)

        player.draw(screen)
        player.update()


        pygame.display.update()

        # health
        if health <= 0:
            game_over = True
            game_active = False
            health = 3
            score = 0
            level = 0
            counter = 0
            fruit_group.remove(fruit_group.sprites())
           
    elif game_active == False and game_over == False:
        """
        intro screen 
        """
        # draw background
        screen.blit(skyScaled, (0, 0))
        screen.blit(groundScaled, (0, height - 100))

        trees.draw(screen)

        player.draw(screen)

        if display_start():
            game_active = True
        
        if display_quit():
            quit()

        pygame.display.update()
    else:
        """ 
        game over screen 
        """
        tick = pygame.time.get_ticks()
        if tick - time_test >= 1000:
            counter += 1
            time_test = tick
        start_time = int(pygame.time.get_ticks() / 1000)
        game_start = clock.get_time()
        # draw background
        screen.blit(skyScaled, (0, 0))
        screen.blit(groundScaled, (0, height - 100))

        trees.draw(screen)

        player.draw(screen)

        if display_restart():
            game_active = True
            game_over = False
            health = 3
            score = 0
            level = 0
            counter = 0
            fruit_group.remove(fruit_group.sprites())

        if display_quit():
            quit()

        pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(fps)
    dt = clock.tick(60) / 1000

pygame.quit()