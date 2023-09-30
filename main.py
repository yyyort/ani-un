# Example file showing a circle moving on screen
import pygame
from random import randint, choice

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
    def __init__(self, x, y, fallTime):
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
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect(midbottom=(randint(x - 10, x + 10), height / 4))
        self.speed = 50
        self.fallTime = fallTime

        """ self.fallTime = randint(1,3) """
        self.angle = 0

    """ 
    methods for animating the fruit fall
    """
    def gravity(self):
        if self.fallTime > 0:
            self.fallTime -= dt 
        else:
            #self.falling_animation()
            self.rect.y += self.speed * 0.1

    """ 
    fruit animation 
    """
    def spawn_animation(self):
        if self.image.get_height() <= 50 and self.image.get_width() <= 50:
            self.image = pygame.transform.scale_by(self.image, 1.1)

    def falling_animation(self):
            
            if self.angle < 360:
                self.angle += 1 * dt
                self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
            else:
                self.angle -= 1 * dt
                self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
    
    def destroy(self):
        if self.rect.y > height - 100:
            decrement_health()
            self.kill()

    def update(self):
        """ self.spawn_animation() """
        self.gravity()
        self.destroy()

    
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
        self.sway_time = randint(1,2)
        self.sway_flag = False
        self.sway_duration = 2
        

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
            self.sway_duration -= dt
        elif self.sway_flag and self.sway_duration <= 0:        
            self.sway_time = randomnum()
            self.sway_flag = False
            self.sway_duration = 2

    """ 
    method for flagging when the tree should sway 
    """
    def to_sway(self):
        """ print(self.sway_time) """
        if self.sway_time > 0 and self.sway_flag == False:
            self.sway_time -= dt
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


""" 
functions
"""
#randomnum
def randomnum():
    num = randint(5, 7)
    return num

#collision
def collision():
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

def display_time():
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
player.add(Player())

fruit_group = pygame.sprite.Group()

#tree setup
tree1 = (100, height - 50)
tree2 = (300, height - 50)
tree3 = (width/2, height - 50)
tree4 = (width - 300, height - 50)
tree5 = (width - 100, height - 50)


trees = pygame.sprite.Group()
trees.add(Tree(tree1[0], tree1[1]))
trees.add(Tree(tree2[0], tree2[1]))
trees.add(Tree(tree3[0], tree3[1]))
trees.add(Tree(tree4[0], tree4[1]))
trees.add(Tree(tree5[0], tree5[1]))

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
            fruit_group.add(choice([Fruit(x=tree.rect.centerx, y=100, fallTime=tree.sway_time) for tree in trees]))

        
        
            
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
        
        if collision():
            score += 1

        display_score(score)
        display_health()
        display_level(level)
        display_time()

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