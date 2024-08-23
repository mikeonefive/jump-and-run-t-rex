import pygame

pygame.init()

screen = pygame.display.set_mode((800, 450))
# ITEMS
house = pygame.image.load("assets/backgrounds/house1.png").convert_alpha()
stand = pygame.image.load("assets/backgrounds/stand.png").convert_alpha()
streetlights = pygame.image.load("assets/backgrounds/streetlights.png").convert_alpha()
boxes = pygame.image.load("assets/backgrounds/boxes.png").convert_alpha()
hydrant = pygame.image.load("assets/backgrounds/hydrant.png").convert_alpha()
bottle = pygame.image.load("assets/backgrounds/bottle.png").convert_alpha()
tires = pygame.image.load("assets/backgrounds/tires.png").convert_alpha()
