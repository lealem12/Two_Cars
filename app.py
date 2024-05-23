
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
middle_line = 20 # the yellow double-line in the middle is 20 px
lane_width = (screen_width - middle_line)//4
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2 CARS")


fps = 80
clock = pygame.time.Clock()


#images
background_lane = pygame.image.load("img/background_lane.png")
background_lane = pygame.transform.scale(background_lane, (screen_width, screen_height + lane_divider))


blue_car = pygame.image.load("img/blue_car.png")
blue_car = pygame.transform.scale(blue_car, (car_width, car_height))
green_car = pygame.image.load("img/green_car.png")
green_car = pygame.transform.scale(green_car, (car_width, car_height))


#main game loop

while running:
    clock.tick(fps)
    
    #drawing backrounds and cars
    screen.blit(background_lane, (0, ground_scroll - lane_divider))
    ground_scroll += scroll_speed
    if ground_scroll > lane_divider:
        ground_scroll = 0


    screen.blit(blue_car, (lane_width + (lane_width - car_width)/2, screen_height - 1.1 * car_height))
    screen.blit(green_car, (2 * lane_width + middle_line + (lane_width - car_width)/2, screen_height - 1.1 * car_height))
    
    
    
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()



