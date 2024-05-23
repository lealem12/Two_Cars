
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
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]



car_group = pygame.sprite.Group()
green_car = Cars(green_car_img, 7/8 * screen_width, screen_height - 0.6 * car_height) # (1 - 1/8) * screen width
blue_car = Cars(blue_car_img, 1/8 * screen_width, screen_height - 0.6 * car_height)
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


       
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()




