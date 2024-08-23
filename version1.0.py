import pygame
import sys
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FPS = 60


# TIME & FONT
def display_time_and_calculate_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000

    time_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 40)
    time_surface = time_font.render(f"{current_time:.1f}", False, "yellow")
    time_rectangle = time_surface.get_rect(center=(73, 63))
    screen.blit(time_surface, time_rectangle)
    return current_time

# initializes pygame, initiates all the things (images, sounds) we need
pygame.init()
pygame.joystick.init()

# store joysticks in list
joysticks = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump and run and jump and run, T-Rex!")
clock = pygame.time.Clock()     # clock for the framerate
is_game_active = False
start_time = 0
score = 0

# BACKGROUND SURFACE
city_surface = pygame.image.load("assets/backgrounds/city1_800.png").convert_alpha()

# ENEMIES SURFACES
# rectangles are for position and collisions (get_rect creates the exact same size as the surface)
human1_surface = pygame.image.load("assets/enemies/humanA0.png").convert_alpha()
human1_rectangle = human1_surface.get_rect(midbottom=(400, 400))
human2_surface = pygame.image.load("assets/enemies/humanB0.png").convert_alpha()
human2_rectangle = human2_surface.get_rect(midbottom=(400, 400))
fly_surface = pygame.image.load("assets/enemies/fly0.png").convert_alpha()


# PLAYER SURFACES & ATTRIBUTES
player_surface = pygame.image.load("assets/player/trex0.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(50, 400))
# create gravity for player for falling (we fall faster the longer we fall)
player_gravity = 0
player_speed = 5

# GAME OVER/INTRO SCREEN SURFACES
player_gameover_scaled = pygame.transform.rotozoom(player_surface, 0, 1.6)
player_gameover_rectangle = player_gameover_scaled.get_rect(center=(400, 225))

game_over_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 60)
game_over_surface = game_over_font.render("game over", False, "yellow")
game_over_rectangle = game_over_surface.get_rect(center=(400, 60))
press_start_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 30)
press_start_surface = press_start_font.render("press start to play again", False, "yellow")
press_start_rectangle = press_start_surface.get_rect(center=(400, 390))

is_main_loop_running = True
# MAIN GAME LOOP, entire game runs in this loop
while is_main_loop_running:

    if is_game_active:
        # draw background and score
        screen.blit(city_surface, (0, 0))   # blit puts 1 surface on another, order matters (background first)
        score = display_time_and_calculate_score()

        # PLAYER
        # increase player's gravity with each loop & increase y position -> falling constantly to have gravity
        player_gravity += 1.5
        player_rectangle.y += player_gravity

        # every time player falls below ground because of increasing gravity put them back on the ground
        if player_rectangle.bottom > 400:
            player_rectangle.bottom = 400
        # # if player jumps out of sight (screen's height)
        # if player_rectangle.top < 0:
        #     player_rectangle.top = 0

        screen.blit(player_surface, player_rectangle)   # take player surface and place it in pos of player rectangle

        # ENEMIES/OBSTACLES MOVEMENT
        # enemy moving & draw them
        human1_rectangle.x -= 4         # grab x coordinate of the rect and move it before draw the image -> in loop -> looks like it's moving
        if human1_rectangle.right <= 0:  # check if right margin of rectangle already off-screen
            human1_rectangle.left = 800  # then place enemy again on left side of the screen -> reappear
        screen.blit(human1_surface, human1_rectangle)

        human2_rectangle.x -= 3
        if human2_rectangle.right <= 0:
            human2_rectangle.left = 1500
        screen.blit(human2_surface, human2_rectangle)

        # collision?
        if player_rectangle.colliderect(human1_rectangle) or player_rectangle.colliderect(human2_rectangle):
            is_game_active = False

        # mouse_position = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_position):
        #     print("collision with mouse!")

        # check for joystick analog stick input, has to be in game loop (NOT event handler),
        # event handler only updates if pos changes so we wouldn't be able to hold a button/stick and have player move
        for joystick in joysticks:
            # left & right (x-axis)
            axis_value_x = joystick.get_axis(0)
            player_rectangle.x += axis_value_x * player_speed
            # up & down (y-axis)
            axis_value_y = joystick.get_axis(1)
            player_rectangle.y += axis_value_y * player_speed

            # d-pad input, check for d-pad directions
            if joystick.get_hat(0) == (1, 0):  # right
                player_rectangle.x += player_speed
            if joystick.get_hat(0) == (-1, 0):  # left
                player_rectangle.x -= player_speed
            if joystick.get_hat(0) == (0, -1):  # up
                player_rectangle.y += player_speed
            if joystick.get_hat(0) == (0, 1):  # down
                player_rectangle.y -= player_speed

            # check for joystick button input, pygame has button numbers for the joystick's buttons
            # check if jump was pressed and if player is on the ground (not already in the air)
            if joystick.get_button(0) == 1 and player_rectangle.bottom >= 400:
                player_gravity = -30

    # GAME OVER SCREEN if current game not active
    else:
        screen.fill("black")
        screen.blit(player_gameover_scaled, player_gameover_rectangle)

        score_message_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 40)
        score_message_surface = score_message_font.render(f"your score: {score:.0f}00", False, "yellow")
        score_message_rectangle = score_message_surface.get_rect(center=(400, 345))

        screen.blit(game_over_surface, game_over_rectangle)
        screen.blit(press_start_surface, press_start_rectangle)
        screen.blit(score_message_surface, score_message_rectangle)

    # UPDATE everything (that was drawn on the screen)
    pygame.display.update()
    clock.tick(FPS)      # control the framerate, so the while loop won't run faster than 60fps

    # EVENT HANDLER
    for event in pygame.event.get():
        # GAME WINDOW
        # if window is closed quit the game
        if event.type == pygame.QUIT:
            is_main_loop_running = False
            pygame.quit()
            sys.exit()  # need to exit here because otherwise pygame.display.update() would cause an error

        # if joystick is plugged in, add it to the joysticks list
        if event.type == pygame.JOYDEVICEADDED:
            joysticks.append(pygame.joystick.Joystick(event.device_index))

        if is_game_active:
            # KEYBOARD
            # check for keyboard input (space bar)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 400:
                    player_gravity = -30

            # MOUSE
            # check if any mouse button was pressed and then if that pos collides with
            # the player (= user clicks on player)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 400:
                    player_gravity = -30

            # useful to get the mouse's position!
            # if event.type == pygame.MOUSEMOTION:
            #     print(event.pos)

        # if game not active and user presses START or SPACE -> start game again
        else:
            if ((event.type == pygame.JOYBUTTONDOWN and event.button == 7)
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                is_game_active = True
                human1_rectangle.left = 800
                human2_rectangle.left = 1600
                start_time = pygame.time.get_ticks()
