
from typing import Any
import pygame
from pygame.locals import *
import random

# game variables
running = True
ground_scroll = 0
scroll_speed = 4
lane_divider = 42 # length of each short, white lane dividers
game_over = False

next_obj = 0
distance_bn_objs = 0
velocity = 4
randomize = False

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


# car groups
class Cars(pygame.sprite.Sprite):
    def __init__(self, image, x, y, car_num):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.car_num = car_num # green car = car#1 and blue car = car#2
        self.clicked = False
        self.change_lanes = False
        self.counter = 0
        self.vel = 4

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
                self.rect.x += self.vel
            elif self.on_right:
                self.rect.x -= self.vel
            self.counter += self.vel

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 4


    def update(self):
        self.rect.y += self.vel

        if self.rect.top > screen_height:
            self.kill()




"""
    create circle and rects at top
    scroll it downward
    when obj position reaches car:
        if obj.img == circle:
            check for collide and kill circle
        if obj.img == rect:
            check for collide and game over

    kill when obj ran outside the screen
    
"""

car_group = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
green_car = Cars(green_car_img, 1/8 * screen_width, screen_height - 0.6 * car_height, 1) 
blue_car = Cars(blue_car_img, 7/8 * screen_width, screen_height - 0.6 * car_height, 2) # (1 - 1/8) * screen width
car_group.add(green_car)
car_group.add(blue_car)



#main game loop
while running:
    clock.tick(fps)
    
    #drawing backrounds and cars
    screen.blit(background_lane, (0, ground_scroll - lane_divider))
    car_group.draw(screen)
    car_group.update()

    
    
    if not(game_over):
        # sliding ground downwards
        ground_scroll += scroll_speed
        if ground_scroll > lane_divider:
            ground_scroll = 0

        # generate obstacles
        if randomize:
            next_obj = random.randint(250, 500)
            randomize = False
        obstacle_type = [circle, rectangle]
        if distance_bn_objs >= next_obj:
            randomize = True
            distance_bn_objs = 0
            random_lane = random.randint(0, 1)
            random_obstacle = random.randint(0, 1)
            obstacle_left = Obstacles(obstacle_type[random_obstacle], 1/8 * screen_width + random_lane * lane_width, 0)
            
            random_lane = random.randint(2, 3)
            random_obstacle = random.randint(0, 1)
            random_y = random.randint(50, 150)
            obstacle_right = Obstacles(obstacle_type[random_obstacle], 1/8 * screen_width + random_lane * lane_width, -1 * random_y)
            
            obstacles_group.add(obstacle_left)
            obstacles_group.add(obstacle_right)
        distance_bn_objs += velocity
        obstacles_group.draw(screen)
        obstacles_group.update()
    

    
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()


