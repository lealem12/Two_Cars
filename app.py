
import pygame
from pygame.locals import *



# screen and functionality
screen_width = 350
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2 CARS")


#images
background_lane = pygame.image.load("img/background_lane.png")
background_lane = pygame.transform.scale(background_lane, (screen_width, screen_height))

# game variables
running = True



#main game loop

while running:
    print("Hello")
    screen.blit(background_lane, (0, 0))


    pygame.display.update()
    
    



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




pygame.quit()













