import pygame
import random


class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_kind):        # enemy_kind specifies the type of enemy fly or human
        super().__init__()

        if enemy_kind == "fly":
            fly_frame1 = pygame.image.load("assets/enemies/superman0.png").convert_alpha()
            fly_frame2 = pygame.image.load("assets/enemies/superman1.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_position = random.randint(220, 270)

        elif enemy_kind == "human1":
            human1_frame1 = pygame.image.load("assets/enemies/humanA0.png").convert_alpha()
            human1_frame2 = pygame.image.load("assets/enemies/humanA1.png").convert_alpha()
            self.frames = [human1_frame1, human1_frame2]
            y_position = random.randint(390, 445)

        else:
            human2_frame1 = pygame.image.load("assets/enemies/humanB0.png").convert_alpha()
            human2_frame2 = pygame.image.load("assets/enemies/humanB1.png").convert_alpha()
            self.frames = [human2_frame1, human2_frame2]
            y_position = random.randint(390, 445)

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1300), y_position))
        self.speed = random.randint(5, 10)

    def animate_enemy(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animate_enemy()
        self.rect.x -= self.speed
        self.kill_offscreen_enemy()

    def kill_offscreen_enemy(self):
        if self.rect.x <= -200:         # if the sprite goes off screen it's going to kill itself
            self.kill()
