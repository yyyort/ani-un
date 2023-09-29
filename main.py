# Example file showing a circle moving on screen
import pygame
from random import randint, choice

#constants
width = 1280
height = 720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
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

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed * dt

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
class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
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
        self.image = pygame.image.load(fruits[randint(0, 6)]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(midbottom=(randint(x - 10, x + 10), height / 4))
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
        if self.rect.y > height - 100:
            decrement_health()
            self.kill()

class Tree(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        tree_n = pygame.image.load("assets/tree/1.png").convert_alpha()
        tree_s = pygame.image.load("assets/tree/2.png").convert_alpha()
        self.tree_frames = [tree_n, tree_s]
        self.tree_index = 0
        self.image = self.tree_frames[self.tree_index]
        self.image = pygame.transform.scale(self.image, (200, height - 100))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.sway_time = self.randomize()
        self.sway_flag = False
        self.sway_duration = 2
    
    def randomize(self):
        return randint(5, 7)

    def animation_state(self):
        print(self.sway_flag)
        if self.sway_flag and self.sway_duration > 0:
            self.sway()
            self.sway_duration -= dt
        elif self.sway_flag and self.sway_duration <= 0:
            self.sway_time = self.randomize()
            self.sway_flag = False
            self.sway_duration = 2

    def to_sway(self):
        print(self.sway_time)
        if self.sway_time > 0 and self.sway_flag == False:
            self.sway_time -= dt
            self.sway_flag = False
            self.sway_duration = 2
        else:
            self.sway_flag = True

    def sway(self):
        self.tree_index += dt
        if self.tree_index >= len(self.tree_frames):
            self.tree_index = 0
        self.image = self.tree_frames[int(self.tree_index)]
        self.image = pygame.transform.scale(self.image, (200, height - 100))
        

    def update(self):
        self.to_sway()
        self.animation_state()

score = 0
health = 3

tree1 = (100, height - 50)
tree2 = (width/2, height - 50)
tree3 = (width - 100, height - 50)

#collision
def collision():
    if pygame.sprite.spritecollide(player.sprite, fruit_group, True):
        return True
    else:
        return False
    
#score
def display_score(score):
    score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(width - 100, 50))
    screen.blit(score_surf, score_rect)

hearts = [
            'assets/heart1.png',
            'assets/heart2.png',
            'assets/heart3.png'
        ]

#health
def decrement_health():
  global health
  """ health -= 1 """


def display_health():
    health_surf = pygame.image.load(hearts[health - 1]).convert_alpha()
    health_surf = pygame.transform.scale(health_surf, (300, 50))
    health_rect = health_surf.get_rect(center=(300, 50))
    screen.blit(health_surf, health_rect)




test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky = pygame.image.load("assets/Sky.png").convert()
ground = pygame.image.load("assets/ground.png").convert()


skyScaled = pygame.transform.scale(sky, (width, height))
groundScaled = pygame.transform.scale(ground, (width, 100))

#class setup
player = pygame.sprite.GroupSingle()
player.add(Player())

fruit_group = pygame.sprite.Group()

trees = pygame.sprite.Group()
trees.add(Tree(tree1[0], tree1[1]))
trees.add(Tree(tree2[0], tree2[1]))
trees.add(Tree(tree3[0], tree3[1]))

""" fruit = pygame.sprite.Group()
for i in range(randint(1, 10)):
    fruit.add(Fruit()) """

# timer
fruit_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fruit_timer, 2000)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == fruit_timer and len(fruit_group) < 3:
            fruit_group.add(choice([Fruit(x=tree1[0], y=tree1[1]),
                                    Fruit(x=tree2[0], y=tree2[1]), 
                                    Fruit(x=tree3[0], y=tree3[1])]))

    # draw background
    screen.blit(skyScaled, (0, 0))
    screen.blit(groundScaled, (0, height - 100))
    

    trees.draw(screen)
    trees.update()

    """ fruit.draw(screen)
    fruit.update() """

    #fruit init
    fruit_group.draw(screen)
    fruit_group.update()
    
    if collision():
        score += 1

    display_score(score)
    display_health()

    player.draw(screen)
    player.update()

    pygame.display.update()

    
    # health

    if health <= 0:
        pass
        """ running = False """

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    
    dt = clock.tick(60) / 1000

pygame.quit()