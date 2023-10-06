import pygame
from random import randint, choice

#comvis
import mediapipe as mp
import cv2

#setup mediapipe instance
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

from screeninfo import get_monitors

monitor = get_monitors()

#dynamic setup
width = monitor[0].width
height = monitor[0].height

#static setup
""" width = 700
height = 700 """

ground_y = int(height - ((height * 13.81) / 100)) # height - 100
player_x = int((width * 7.81) / 100) # 100
player_y = int((height * 13.89) / 100) # 100
fruit_x = int((width * 3.91) / 100) # 50
fruit_y = int((height * 6.94) / 100) # 50
tree_x = int((width * 15.63) / 100) # 200
tree_ground = ground_y + fruit_x # ground_y + 50
health_x = int((width * 3.91) / 100) # 50
health_y = int((height * 6.94) / 100) # 50
scale_x_20 = int((width * 1.56) / 100) # 20
scale_y_20 = int((height * 3.47) / 100) # 20
scale_x_50 = int((width * 3.91) / 100) # 50
scale_y_50 = int((height * 6.94) / 100) # 50
scale_x_100 = int((width * 7.81) / 100) # 100
scale_y_100 = int((height * 13.89) / 100) # 100
scale_x_150 = int((width * 11.72) / 100) # 150
scale_y_150 = int((height * 20.83) / 100) # 150
scale_x_200 = int((width * 15.63) / 100) # 200
scale_y_200 = int((height * 27.78) / 100) # 200


#volume
volume = 0.1


# pygame setup
pygame.init()
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
fps = 60
dt = 0
game_active = False
game_over = False

cap = cv2.VideoCapture(0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        player_f = pygame.image.load("assets/player/farmer.png").convert_alpha()
        player_s = pygame.image.load("assets/player/farmer.png").convert_alpha()
        self.player_frames = [player_f, player_s]
        self.player_index = 0
        self.image = self.player_frames[self.player_index]
        self.image = pygame.transform.scale(self.image, (player_x, player_y))
        #self.image = pygame.image.load("assets/player.png").convert_alpha()
        #self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(midbottom=(width / 2, ground_y))
        self.speed = 1000

    def comvis_input(self, x):
        if x > 0 and x < width:
            self.rect.x = x
            
    """ 
    keyboard input
    """
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width:
            self.rect.x += self.speed * dt

    """ 
    methods for animating the player
    """
    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_index = 1
            self.image = self.player_frames[self.player_index]
            self.image = pygame.transform.flip(self.image, True, False)
            self.image = pygame.transform.scale(self.image, (player_x, player_y))
        elif keys[pygame.K_d]:
            self.player_index = 1
            self.image = self.player_frames[self.player_index]
            self.image = pygame.transform.scale(self.image, (player_x, player_y))
        else:
            self.player_index = 0
            self.image = self.player_frames[self.player_index]
            self.image = pygame.transform.scale(self.image, (player_x, player_y))


    """ def movement(self):
        randomx = randint(0, width)
        self.rect.x = randomx """

    def update(self, x = width / 2):
        self.comvis_input(x)
        self.player_input()
        self.animation_state()
        """ self.movement()
 """
class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, fallTime, speed):
        super().__init__()
        fruits = [
            'assets/fruits/apple.png',
            'assets/fruits/cherry-pie.png',
            'assets/fruits/mango.png',
            'assets/fruits/orange.png',
            'assets/fruits/pear.png',
        ]
        self.scale = (fruit_x, fruit_y)
        self.image = pygame.image.load(fruits[randint(0, len(fruits)-1)]).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.scale)
        self.rect = self.image.get_rect(midbottom=(randint(x - 20, x + 20), height / 4))
        self.speed = speed
        self.fallTime = fallTime
        self.drop_sound = pygame.mixer.Sound('assets/sound/drop.wav')
        self.drop_sound.set_volume(volume)
        """ self.fallTime = randint(1,3) """
        self.angle = 0
        

    """ 
    methods for animating the fruit fall
    """
    def gravity(self):
        if self.fallTime > 0:
            self.fallTime -= dt 
        else:
            self.rect.y += self.speed * 0.2

    """ 
    todo add spawn animation
    fall animation 
    """

    """ 
    fruit animation 
    """
    """ def spawn_animation(self):
        if self.scale <= 0.5:
            self.scale += 0.01
            self.image = pygame.transform.scale_by(self.image, self.scale)
        else:
            return False
    """

    """ def falling_animation(self):
            self.angle += 0 * dt
            self.image = pygame.transform.rotate(self.image, self.angle)
            #self.image = pygame.transform.scale(self.image, self.scale)
             """
    
    def destroy(self):
        if self.rect.y > ground_y:
            self.drop_sound.play()
            decrement_health()
            self.kill()

    def update(self):
        #self.spawn_animation()
        #self.falling_animation()
        self.gravity()
        self.destroy()

    
class Tree(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        tree_n = pygame.image.load("assets/tree/tree.png").convert_alpha()
        tree_s = pygame.image.load("assets/tree/tree-slant.png").convert_alpha()
        tree_s2 = pygame.image.load("assets/tree/tree-slant2.png").convert_alpha()
        self.tree_frames = [tree_n, tree_s, tree_s2]
        self.tree_index = 0
        self.image = self.tree_frames[self.tree_index]
        self.image = pygame.transform.scale(self.image, (tree_x, tree_ground))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.sway_time = randint(0,1)
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
        self.tree_index += 0.2
        if self.tree_index >= len(self.tree_frames):
            self.tree_index = 0
        self.image = self.tree_frames[int(self.tree_index)]
        self.image = pygame.transform.scale(self.image, (tree_x, tree_ground))
        
    def update(self):
        """ self.add_fruit() """
        self.to_sway()
        self.animation_state()


""" 
functions
"""
#randomnum
def randomnum():
    num = randint(1, 3)
    return num

#collision
def collision():
    if pygame.sprite.spritecollide(player.sprite, fruit_group, True):
        sound = pygame.mixer.Sound('assets/sound/Pickup.wav')
        sound.set_volume(volume)
        sound.play()
        return True
    else:
        return False
    
#score
def display_score(score):
    score_surf = pixel_font.render(f'Score: {score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(width - scale_x_150, scale_y_50))
    screen.blit(score_surf, score_rect)

#level
def display_level(level):
    level_surf = pixel_font.render(f'Level: {level}', False, (64, 64, 64))
    level_rect = level_surf.get_rect(center=(width - scale_x_150, scale_y_100))
    screen.blit(level_surf, level_rect)

def display_time():
    time_surf = pixel_font.render(f'Time: {int(timer)}', False, (64, 64, 64))
    time_rect = time_surf.get_rect(center=(width - scale_x_150, scale_y_150))
    screen.blit(time_surf, time_rect)


""" 
intro func
"""


#start btn
def display_start():
    start_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_200)
    start_surf = start_font.render(f'Start', False, (64, 64, 64))
    start_rect = start_surf.get_rect(center=(width / 2, height / 2))
    screen.blit(start_surf, start_rect)

    # Check if the start button has been clicked
    if start_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True
        
    if start_rect.collidepoint(mouse_rect.centerx, mouse_rect.centery):
        start_surf = pixel_font.render(f'Start', False, (255, 255, 255), (64, 64, 64))
        return True


#restart btn
def display_restart():
    restart_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_150)
    restart_surf = restart_font.render(f'Restart', False, (64, 64, 64))
    restart_rect = restart_surf.get_rect(center=(width / 2, (height / 2) - scale_y_100 - scale_y_50))
    screen.blit(restart_surf, restart_rect)

    # Check if the start button has been clicked
    if restart_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True
    
    if restart_rect.collidepoint(mouse_rect.centerx, mouse_rect.centery):
        return True

#quit
def display_quit():
    quit_surf = pixel_font.render(f'Quit', False, (64, 64, 64))
    quit_rect = quit_surf.get_rect(center=(width / 2, (height / 2) + scale_y_100))
    screen.blit(quit_surf, quit_rect)

    # Check if the start button has been clicked
    if quit_rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            return True
        
#score
def display_gameover_score(game_over_score):
    score_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_150)
    score_surf = score_font.render(f'Score: {game_over_score}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(width / 2, (height / 2)))
    screen.blit(score_surf, score_rect)

#credit
def display_credit_dev():
    credit_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_20)
    credit_surf = credit_font.render(f'Developers: Ian Troy Pahilga, Shon Mikhael Gesulgon, Christian Jay Allado, Joseph Andrean De La Cruz', False, (255, 255, 255))
    credit_rect = credit_surf.get_rect(center=((width / 4 - 30), ground_y + scale_y_50 + scale_y_20 - 10 ))
    screen.blit(credit_surf, credit_rect)

def display_credit_creatives():
    credit_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_20)
    credit_surf = credit_font.render(f'Creatives: Markuly Chua, Alexandra Cristina Gepes, Diego Paul Leetian', False, (255, 255, 255))
    credit_rect = credit_surf.get_rect(center=(int(width - width/6), ground_y + scale_y_50 + scale_y_20 - 10))
    screen.blit(credit_surf, credit_rect)

hearts = [
            'assets/heart/3.png',
            'assets/heart/2.png',
            'assets/heart/1.png',
        ]

#health
def decrement_health():
  global health
  health -= 1

def display_health():
    if health >= 3:
        health_surf = pygame.image.load(hearts[2]).convert_alpha()
    elif health == 2:
        health_surf = pygame.image.load(hearts[1]).convert_alpha()
    else:
        health_surf = pygame.image.load(hearts[0]).convert_alpha()

    health_surf = pygame.transform.scale(health_surf, (scale_x_100 + scale_x_100, scale_y_50 + scale_y_50))
    health_rect = health_surf.get_rect(center=(health_x + scale_x_100, health_y + scale_y_20))
    screen.blit(health_surf, health_rect)

    """ health_surf = pygame.image.load(hearts[health - 1]).convert_alpha()
    health_surf = pygame.transform.scale(health_surf, (300, 50))
    health_rect = health_surf.get_rect(center=(300, 50))
    screen.blit(health_surf, health_rect)
 """

pixel_font = pygame.font.Font('font/Pixeltype.ttf', scale_x_100)

sky = pygame.image.load("assets/Sky.png").convert()
ground = pygame.image.load("assets/ground.png").convert()


skyScaled = pygame.transform.scale(sky, (width, height))
groundScaled = pygame.transform.scale(ground, (width, tree_ground))

#background
bg1 = pygame.image.load("assets/background/1.png").convert()
bg1 = pygame.transform.scale(bg1, (width, height))
bg2 = pygame.image.load("assets/background/2.png").convert()
bg2 = pygame.transform.scale(bg2, (width, height))
bg3 = pygame.image.load("assets/background/3.png").convert()
bg3 = pygame.transform.scale(bg3, (width, height))
bg4 = pygame.image.load("assets/background/4.png").convert()
bg4 = pygame.transform.scale(bg4, (width, height))
bg5 = pygame.image.load("assets/background/5.png").convert()
bg5 = pygame.transform.scale(bg5, (width, height))

bg_list = [bg1, bg2, bg3, bg4, bg5]

def random_bg():
    return randint(0, len(bg_list)-1)

bg_index = random_bg()

background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (width, height))

mouse = pygame.image.load("assets/mouse.png").convert_alpha()
mouse = pygame.transform.scale(mouse, (scale_x_50, scale_y_50))
mouse_rect = mouse.get_rect(center=(0, 0))


#bg music
pygame.mixer.music.load('assets/sound/Background.mp3')
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(loops = -1)
"""
intro
"""


#class setup
player = pygame.sprite.GroupSingle()
player.add(Player())

fruit_group = pygame.sprite.Group()

#tree setup
tree_list = [
    (width/7, tree_ground),
    (width/3, tree_ground),
    (width/2, tree_ground),
    (int(width -(width/3)), tree_ground),
    (int(width - (width/7)), tree_ground),
]

trees = pygame.sprite.Group()
for tree in tree_list:
    trees.add(Tree(tree[0], tree[1]))

""" 
user events
"""
# timer
fruit_timer = pygame.USEREVENT + 1
pygame.time.set_timer(fruit_timer, 2000)

#constants
score = 0
health = 3
level = 0

#time
time_test = pygame.time.get_ticks()
counter = 0
timer = 0

#levels
fruit_spawn = 3
fruit_fall_speed = 50

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  
  
  while cap.isOpened() and running: 
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

   
    image.flags.writeable = False
    image = cv2.flip(image,1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
    
    cv2.imshow('MediaPipe Pose',image)

    if cv2.waitKey(5) & 0xFF == 27:
      break

    print(clock.get_fps())
    print(f'dt {dt}')

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
        if game_active:
            if event.type == fruit_timer and len(fruit_group) < fruit_spawn:
                fruit_group.add(choice([Fruit(x=tree.rect.centerx, y=100, fallTime=(tree.sway_time+0.5), speed=fruit_fall_speed) for tree in trees]))

    if game_active:
        tick = pygame.time.get_ticks()
        if tick - time_test >= 1000:
            timer += 1
            counter += 1
            time_test = tick
        
        if counter >= 60:
            level += 1
            fruit_spawn += 1
            fruit_fall_speed += 10
            counter = 0

        start_time = int(pygame.time.get_ticks() / 1000)

        # draw background
        screen.blit(bg_list[bg_index], (0, 0, width, height))
        #screen.blit(background, (0, 0, width, height))
        #screen.blit(skyScaled, (0, 0))
        #screen.blit(groundScaled, (0, height - 100))

        trees.draw(screen)
        trees.update()

        #fruit init
        fruit_group.draw(screen)
        fruit_group.update()
        
        if collision():
            score += 1

        display_score(score)
        display_level(level)
        display_time()

        display_health()

        if results.pose_landmarks is not None:
            nose_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
            nose_x_flipped = nose_x
            player.update(nose_x_flipped * width)
        else:
            print("No person detected.")

        player.draw(screen)

        pygame.display.update()
        
        # health
        if health <= 0:
            game_over = True
            game_active = False
            health = 3
            level = 0
            timer = 0
            counter = 0
            bg_index = random_bg()
            #level props
            fruit_spawn = 3
            fruit_fall_speed = 50

            fruit_group.remove(fruit_group.sprites())
           
    elif game_active == False and game_over == False:
        """
        intro screen 
        """

        # draw background
        screen.blit(bg_list[bg_index], (0, 0, width, height))
        #screen.blit(background, (0, 0, width, height))
        """ screen.blit(skyScaled, (0, 0))
        screen.blit(groundScaled, (0, height - 100)) """

        trees.draw(screen)

        player.draw(screen)

        display_credit_dev()
        display_credit_creatives()

        if display_start():
            bg_index = random_bg()
            game_active = True
        
        if results.pose_landmarks is not None:
            r_index_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x
            r_index_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y
            
            mouse_rect.centerx = (r_index_x * width)
            mouse_rect.centery = (r_index_y * height)
            screen.blit(mouse, (r_index_x * width, r_index_y * height))
            
        else:
            print("No person detected.")

        pygame.display.update()

    else:
        """ 
        game over screen 
        """
        tick = pygame.time.get_ticks()
        if tick - time_test >= 1000:
            counter += 1
            time_test = tick

        if counter >= 30:
            game_over = False
            counter = 0

        start_time = int(pygame.time.get_ticks() / 1000)
        game_start = clock.get_time()
        # draw background
        screen.blit(bg_list[bg_index], (0, 0, width, height))
        #screen.blit(background, (0, 0, width, height))
        """ screen.blit(skyScaled, (0, 0))
        screen.blit(groundScaled, (0, height - 100)) """

        trees.draw(screen)

        player.draw(screen)

        display_gameover_score(score)

        display_credit_dev()
        display_credit_creatives()

        if display_restart():
            game_active = True
            game_over = False
            health = 3
            score = 0
            level = 0
            counter = 0
            timer = 0
            bg_index = random_bg()
            #level props
            fruit_spawn = 3
            fruit_fall_speed = 50

            fruit_group.remove(fruit_group.sprites())

        if results.pose_landmarks is not None:
            r_index_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x
            r_index_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y
            
            mouse_rect.centerx = (r_index_x * width)
            mouse_rect.centery = (r_index_y * height)
            screen.blit(mouse, (r_index_x * width, r_index_y * height))
            
        else:
            print("No person detected.")

        pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    clock.tick(fps)
    dt = clock.tick(60) / 1000

pygame.quit()
cap.release()
cv2.destroyAllWindows()