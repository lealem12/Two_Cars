
import pygame
from pygame.locals import *



# screen and functionality
screen_width = 400
screen_height = 500
car_width = 60
car_height = 135
# the middle double-line is 20 px
middle_line = 20
lane_width = (screen_width - middle_line)//4 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2 CARS")


#images
background_lane = pygame.image.load("img/background_lane.png")
background_lane = pygame.transform.scale(background_lane, (screen_width, screen_height))

blue_car = pygame.image.load("img/blue_car.png")
blue_car = pygame.transform.scale(blue_car, (car_width, car_height))
green_car = pygame.image.load("img/green_car.png")
green_car = pygame.transform.scale(green_car, (car_width, car_height))

# game variables
running = True



#main game loop

while running:
    
    #drawing backrounds and cars
    screen.blit(background_lane, (0, 0))
    screen.blit(blue_car, (lane_width + (lane_width - car_width)/2, screen_height - 1.1 * car_height))
    screen.blit(green_car, (2 * lane_width + middle_line + (lane_width - car_width)/2, screen_height - 1.1 * car_height))
    
    
    
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()













