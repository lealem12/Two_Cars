 
from typing import Any
import pygame
from pygame.locals import *
import random


pygame.font.init()

# game variables
running = True
ground_scroll = 0
scroll_speed = 4
lane_divider = 42 # length of each short, white lane dividers
game_over = False
driving = False

next_obj = 0
distance_bn_objs = 0
velocity = 4
randomize = False
score = 0
font = pygame.font.SysFont("Bauhaus 93", 60)
white = (255, 255, 255)

# screen and functionality
screen_width = 400
screen_height = 500
car_width = 44
car_height = 100
lane_width = screen_width//4
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2 CARS")

fps = 80
clock = pygame.time.Clock()



#images
background_lane = pygame.transform.scale(pygame.image.load("img/background_lane.png"), (screen_width, screen_height + lane_divider))
blue_car_img = pygame.transform.scale(pygame.image.load("img/blue_car.png"), (car_width, car_height))
green_car_img = pygame.transform.scale(pygame.image.load("img/green_car.png"), (car_width, car_height))

circle = pygame.transform.scale(pygame.image.load("img/circle.png"), (40, 40))
rectangle = pygame.transform.scale(pygame.image.load("img/rectangle.png"), (40, 40))

def draw_text(text, font, text_color, x, y):
    msg = font.render(text, True, text_color)
    screen.blit(msg, (x, y))

def reset_game():

    goodies_group.empty()
    obstacles_group.empty()

    green_car.rect.center = [1/8 * screen_width, screen_height - 0.6 * car_height]
    blue_car.rect.center = [7/8 * screen_width, screen_height - 0.6 * car_height]
    green_car.on_left = True
    green_car.on_right = False
    blue_car.on_left = True
    blue_car.on_right = False

    score = 0
    return score


# car groups
class Cars(pygame.sprite.Sprite):
    def __init__(self, image, x, y, car_num):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.car_num = car_num # green car = car#1 and blue car = car#2
        self.clicked = False
        self.on_left = True
        self.on_right = False
        self.change_lanes = False
        self.counter = 0

    def update(self):
        # assign keyboard keys to each car.
        if self.car_num == 1:
            self.index = K_1
        elif self.car_num == 2:
            self.index = K_2
        # check interaction with keyboard
        if self.clicked == False and self.change_lanes == False and pygame.key.get_pressed()[self.index] == True:
            self.clicked = True
            self.change_lanes = True
        if pygame.key.get_pressed()[self.index] == False:
            self.clicked = False
        
        if self.counter >= lane_width:
            self.change_lanes = False
            self.counter = 0
        
        if self.car_num == 1:
            self.crossing_line = 1/4 * screen_width
        elif self.car_num == 2:
            self.crossing_line = 3/4 * screen_width
        
        if self.change_lanes == False and self.rect.x <= self.crossing_line:
            self.on_left = True
            self.on_right = False
        elif self.change_lanes == False and self.rect.x >= self.crossing_line:
            self.on_left = False
            self.on_right = True

        if self.change_lanes == True:

            if self.on_left:
                self.rect.x += velocity
            elif self.on_right:
                self.rect.x -= velocity
            self.counter += velocity

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        self.rect.y += velocity

        if self.rect.top > screen_height:
            self.kill()


class Button():
    def __init__(self, img, x, y):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        cursor_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(cursor_position) == 1:
            if pygame.mouse.get_pressed()[0]:
                return True
            
car_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
goodies_group = pygame.sprite.Group()
green_car = Cars(green_car_img, 1/8 * screen_width, screen_height - 0.6 * car_height, 1) 
blue_car = Cars(blue_car_img, 7/8 * screen_width, screen_height - 0.6 * car_height, 2) # (1 - 1/8) * screen width
car_group.add(green_car)
car_group.add(blue_car)

restart_btn = Button("img/restart.png", screen_width//2, screen_height//2 - 30)

#main game loop
while running:
    clock.tick(fps)
    
    #drawing backrounds and cars
    screen.blit(background_lane, (0, ground_scroll - lane_divider))
    car_group.draw(screen)    
    obstacles_group.draw(screen)
    goodies_group.draw(screen)

  
    
    if not(game_over) and driving:
        # sliding ground downwards
        ground_scroll += scroll_speed
        if ground_scroll > lane_divider:
            ground_scroll = 0

        # generate obstacles
        if randomize:
            next_obj = random.randint(250, 499)
            randomize = False
        if distance_bn_objs >= next_obj:
            randomize = True
            distance_bn_objs = 0
            random_lane = random.randint(0, 1)
            random_obj = random.randint(0, 1)
            if random_obj == 0:
                obstacle_left = Obstacles(rectangle, 1/8 * screen_width + random_lane * lane_width, 0)
                obstacles_group.add(obstacle_left)
            else:
                goody_left = Obstacles(circle, 1/8 * screen_width + random_lane * lane_width, 0)
                goodies_group.add(goody_left)
            
            random_lane = random.randint(2, 3)
            random_obj = random.randint(0, 1)
            random_y = random.randint(50, 150)
            if random_obj == 0:
                obstacle_right = Obstacles(rectangle, 1/8 * screen_width + random_lane * lane_width, -1 * random_y)
                obstacles_group.add(obstacle_right)
            else:
                goody_right = Obstacles(circle, 1/8 * screen_width + random_lane * lane_width, -1 * random_y)
                goodies_group.add(goody_right)            

        distance_bn_objs += velocity

        if  len(obstacles_group) > 0 or len(goodies_group) > 0:
            if pygame.sprite.groupcollide(car_group, obstacles_group, False, True):
                game_over = True
                driving = False
            elif pygame.sprite.groupcollide(car_group, goodies_group, False, True):
                score += 1

        goodies_group.update()
        obstacles_group.update()
        car_group.update()
    
    draw_text(str(score), font, white, screen_width//2 - 50, 20)
    if not(driving) and not(game_over):
        draw_text("Press any key", font, white, 20, screen_height//2 - 120)
        draw_text("to start...", font, white, lane_width - 30, screen_height//2 - 60)

    if game_over:
        if restart_btn.draw():
            game_over = False
            score = reset_game()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not(driving) and not(game_over) and event.type == pygame.KEYDOWN:
            driving = True
    
    pygame.display.update()


pygame.quit()


