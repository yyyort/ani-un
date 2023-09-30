import pygame
from random import randint, choice

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

""" 
functions
"""
#randomnum
def randomnum():
    num = randint(5, 7)
    return num

#collision
def collision(player, fruit_group):
    if pygame.sprite.spritecollide(player.sprite, fruit_group, True):
        return True
    else:
        return False
    
#score
def display_score(score):
    score_surf = pixel_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(width - 100, 50))
    screen.blit(score_surf, score_rect)

#level
def display_level(level):
    level_surf = pixel_font.render(f'Level: {level}', False, (64, 64, 64))
    level_rect = level_surf.get_rect(center=(width - 100, 100))
    screen.blit(level_surf, level_rect)

def display_time(counter):
    time_surf = pixel_font.render(f'Time: {int(counter)}', False, (64, 64, 64))
    time_rect = time_surf.get_rect(center=(width - 100, 150))
    screen.blit(time_surf, time_rect)


""" 
intro func
"""

#start btn
def display_start():
    start_surf = pixel_font.render(f'Start', False, (64, 64, 64))
    start_rect = start_surf.get_rect(center=(width / 2, height / 2))
    screen.blit(start_surf, start_rect)

    # Check if the start button has been clicked
    if start_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True

#restart btn
def display_restart():
    restart_surf = pixel_font.render(f'Restart', False, (64, 64, 64))
    restart_rect = restart_surf.get_rect(center=(width / 2, height / 2))
    screen.blit(restart_surf, restart_rect)

    # Check if the start button has been clicked
    if restart_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True

#quit
def display_quit():
    quit_surf = pixel_font.render(f'Quit', False, (64, 64, 64))
    quit_rect = quit_surf.get_rect(center=(width / 2, (height / 2) + 100))
    screen.blit(quit_surf, quit_rect)

    # Check if the start button has been clicked
    if quit_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True

hearts = [
            'assets/heart1.png',
            'assets/heart2.png',
            'assets/heart3.png'
        ]

#health
def decrement_health():
  global health
  health -= 1

def display_health():
    health_surf = pygame.image.load(hearts[health - 1]).convert_alpha()
    health_surf = pygame.transform.scale(health_surf, (300, 50))
    health_rect = health_surf.get_rect(center=(300, 50))
    screen.blit(health_surf, health_rect)
