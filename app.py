
from typing import Any
import pygame
from pygame.locals import *

# game variables
running = True
ground_scroll = 0
scroll_speed = 4
lane_divider = 42 # length of each short, white lane dividers


# screen and functionality
screen_width = 400
screen_height = 500
car_width = 60
car_height = 135
lane_width = screen_width//4
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2 CARS")

fps = 80
clock = pygame.time.Clock()




#images
background_lane = pygame.image.load("img/background_lane.png")
background_lane = pygame.transform.scale(background_lane, (screen_width, screen_height + lane_divider))

blue_car_img = pygame.transform.scale(pygame.image.load("img/blue_car.png"), (car_width, car_height))
green_car_img = pygame.transform.scale(pygame.image.load("img/green_car.png"), (car_width, car_height))


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


car_group = pygame.sprite.Group()
green_car = Cars(green_car_img, 1/8 * screen_width, screen_height - 0.6 * car_height, 1) 
blue_car = Cars(blue_car_img, 7/8 * screen_width, screen_height - 0.6 * car_height, 2) # (1 - 1/8) * screen width
car_group.add(green_car)
car_group.add(blue_car)


#main game loop
while running:
    clock.tick(fps)
    
    #drawing backrounds and cars
    screen.blit(background_lane, (0, ground_scroll - lane_divider))
    ground_scroll += scroll_speed
    if ground_scroll > lane_divider:
        ground_scroll = 0

    # draw cars and obstacles
    car_group.draw(screen)
    car_group.update()
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()




