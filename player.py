import pygame


class Player(pygame.sprite.Sprite):     # inherits from sprite class

    def __init__(self, joysticks):
        super().__init__()

        # PLAYER SURFACES & ATTRIBUTES
        player_walk0 = pygame.image.load("assets/player/trex1.png").convert_alpha()
        player_walk1 = pygame.image.load("assets/player/trex2.png").convert_alpha()
        self.player_walk = [player_walk0, player_walk1]     # self because we wanna access these outside of init method
        self.player_index = 0
        self.player_jump = pygame.image.load("assets/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 400))

        self.gravity = 0
        self.speed = 5
        self.joysticks = joysticks

        self.jump_sound = pygame.mixer.Sound("sounds/8bitJump.wav")

    def apply_gravity(self):
        self.gravity += 1.5
        self.rect.y += self.gravity
        # every time player falls below ground because of increasing gravity put them back on the ground
        if self.rect.bottom > 400:
            self.rect.bottom = 400

    def handle_input(self):
        # JOYSTICK INPUT
        for joystick in self.joysticks:
            # left & right (x-axis)
            axis_value_x = joystick.get_axis(0)
            self.rect.x += axis_value_x * self.speed
            # up & down (y-axis)
            axis_value_y = joystick.get_axis(1)
            self.rect.y += axis_value_y * self.speed

            # d-pad input, check for d-pad directions
            if joystick.get_hat(0) == (1, 0):  # right
                self.rect.x += self.speed
            if joystick.get_hat(0) == (-1, 0):  # left
                self.rect.x -= self.speed

            # check if jump was pressed and if player is on the ground (not already in the air)
            if joystick.get_button(0) == 1 and self.rect.bottom >= 400:
                self.gravity = -30
                self.jump_sound.play()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -30
            self.jump_sound.play()

        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed

        mouse_button_pressed = pygame.mouse.get_pressed()
        if mouse_button_pressed[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()) and self.rect.bottom >= 400:
                self.gravity = -30
                self.jump_sound.play()

    def animate_player(self):
        if self.rect.x < 0:             # if player off screen
            self.rect.x = 0

        if self.rect.bottom < 400:      # if player in the air display jump frame
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            # increase index slowly and make sure we don't access out of range
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.animate_player()
