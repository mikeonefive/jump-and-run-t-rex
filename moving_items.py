import pygame
import random


class MovingItems(pygame.sprite.Sprite):

    def __init__(self, item_kind):
        super().__init__()

        match item_kind:
            case "house":
                self.image = pygame.image.load("assets/backgrounds/house1.png").convert_alpha()
                x_position = 1500
                y_position = 430
            case "stand":
                self.image = pygame.image.load("assets/backgrounds/stand.png").convert_alpha()
                x_position = 1500
                y_position = 470
            case "streetlights":
                self.image = pygame.image.load("assets/backgrounds/streetlights.png").convert_alpha()
                x_position = 1700
                y_position = 500
            case "boxes":
                self.image = pygame.image.load("assets/backgrounds/boxes.png").convert_alpha()
                x_position = 1700
                y_position = 480
            case "hydrant":
                self.image = pygame.image.load("assets/backgrounds/hydrant.png").convert_alpha()
                x_position = 1700
                y_position = 490
            case "bottle":
                self.image = pygame.image.load("assets/backgrounds/bottle.png").convert_alpha()
                x_position = 1700
                y_position = 550
            case "tires":
                self.image = pygame.image.load("assets/backgrounds/tires.png").convert_alpha()
                x_position = 1700
                y_position = 480

        self.rect = self.image.get_rect(midbottom=(x_position, y_position))
        self.speed = 4

    def update(self):
        self.rect.x -= self.speed
        self.kill_offscreen_item()

    def kill_offscreen_item(self):
        if self.rect.x <= -500:
            self.kill()
