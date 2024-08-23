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


# function for enemies and generating different starting pos for them in the obstacle list
def move_obstacles(obstacle_list):
    obstacle_speed = random.randint(1, 8)
    if obstacle_list:   # if the list is not empty, move every obstacle a little to the left
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= obstacle_speed

            # draw a fly enemy surface at this position we know 270 is a fly because it's higher
            if obstacle_rectangle.bottom <= 270:
                screen.blit(fly_surface, obstacle_rectangle)
            # remainder of division based on x position just to have a random choice between human skins
            # 'cause we can't have anything in the game loop it would change constantly
            elif obstacle_rectangle.y % 2 == 0:
                screen.blit(human1_surface, obstacle_rectangle)
            else:
                screen.blit(human2_surface, obstacle_rectangle)

        # only copy obstacles to the list if obstacle is on screen (x > 0) otherwise list would grow and slow down game
        new_obstacle_list = []
        for obstacle in obstacle_list:
            if obstacle.x > -100:
                new_obstacle_list.append(obstacle)

        obstacle_list = new_obstacle_list
        return obstacle_list
    # if the list is empty (start of the game cause timer hasn't been triggered) return an empty list NOT None
    else:
        return []


# function for collisions
def check_collisions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True


def animate_player():
    global player_surface, player_index

    if player_rectangle.x < 0:  # if player leaves screen
        player_rectangle.x = 0

    if player_rectangle.bottom < 400:
        player_surface = player_jump
    else:
        player_index += 0.1
        # increase index slowly and make sure we don't access out of range
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


def animate_background():
    global background_scroll
    # endless background scroll
    screen.blit(graywall_surface, (background_scroll, 0))
    screen.blit(graywall_surface, (graywall_surface.get_width() + background_scroll, 0))
    screen.blit(ground_surface, (background_scroll, 0))
    screen.blit(ground_surface, (ground_surface.get_width() + background_scroll, 0))

    # if off screen -get_width() put next image at pos 0
    if background_scroll <= - ground_surface.get_width():
        background_scroll = 0
    background_scroll -= 4  # moving to left with every while loop iteration


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
background_scroll = 0

# BACKGROUND SURFACES & ITEM SURFACES
sky_surface = pygame.image.load("assets/backgrounds/sky.png").convert_alpha()
buildings_surface = pygame.image.load("assets/backgrounds/buildings.png").convert_alpha()
graywall_surface = pygame.image.load("assets/backgrounds/graywall.png").convert_alpha()
ground_surface = pygame.image.load("assets/backgrounds/ground.png").convert_alpha()
house1_surface = pygame.image.load("assets/backgrounds/house1.png").convert_alpha()

# ENEMIES SURFACES
# rectangles are for position and collisions (get_rect creates the exact same size as the surface)
human1_frame1 = pygame.image.load("assets/enemies/humanA0.png").convert_alpha()
human1_frame2 = pygame.image.load("assets/enemies/humanA1.png").convert_alpha()
human1_frames = [human1_frame1, human1_frame2]
human1_frame_index = 0
human1_surface = human1_frames[human1_frame_index]

human2_frame1 = pygame.image.load("assets/enemies/humanB0.png").convert_alpha()
human2_frame2 = pygame.image.load("assets/enemies/humanB1.png").convert_alpha()
human2_frames = [human2_frame1, human2_frame2]
human2_frame_index = 0
human2_surface = human2_frames[human2_frame_index]

fly_frame1 = pygame.image.load("assets/enemies/superman0.png").convert_alpha()
fly_frame2 = pygame.image.load("assets/enemies/superman1.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rectangle_list = []

# PLAYER SURFACES & ATTRIBUTES
player_walk0 = pygame.image.load("assets/player/trex1.png").convert_alpha()
player_walk1 = pygame.image.load("assets/player/trex2.png").convert_alpha()
player_walk = [player_walk0, player_walk1]
player_index = 0
player_jump = pygame.image.load("assets/player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(midbottom=(50, 400))
# create gravity for player for falling (we fall faster the longer we fall)
player_gravity = 0
player_speed = 5

# GAME OVER/INTRO SCREEN SURFACES
player_standing = pygame.image.load("assets/player/trex0.png").convert_alpha()
player_gameover_scaled = pygame.transform.rotozoom(player_standing, 0, 1.5)
player_gameover_rectangle = player_gameover_scaled.get_rect(center=(400, 225))

game_over_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 60)
game_over_surface = game_over_font.render("game over", False, "yellow")
game_over_rectangle = game_over_surface.get_rect(center=(400, 60))
press_start_font = pygame.font.Font("assets/fonts/pixeltype.ttf", 30)
press_start_surface = press_start_font.render("press start to play again", False, "yellow")
press_start_rectangle = press_start_surface.get_rect(center=(400, 390))

# OBSTACLE TIMER (to help us let enemies appear on screen at certain intervals)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, random.randint(3000, 4000))

# HUMAN1 ANIMATION TIMER
human1_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(human1_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

is_main_loop_running = True
# MAIN GAME LOOP, entire game runs in this loop
while is_main_loop_running:

    if is_game_active:
        # draw background and score
        screen.blit(sky_surface, (0, 0))   # blit puts 1 surface on another, order matters (background first)
        screen.blit(buildings_surface, (0, 0))

        animate_background()

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

        animate_player()
        screen.blit(player_surface, player_rectangle)   # take player surface and place it in pos of player rectangle

        # ENEMIES MOVING & COLLISION functions
        obstacle_rectangle_list = move_obstacles(obstacle_rectangle_list)
        is_game_active = check_collisions(player_rectangle, obstacle_rectangle_list)

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
        player_rectangle.midbottom = (100, 400)  # put player back to original start pos (e.g. was jumping at gameover)
        player_gravity = 0

        # empty obstacle list because enemies are still in place after a collision
        # which would trigger another collision right away
        obstacle_rectangle_list.clear()

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

            # ENEMIES/OBSTACLES intervals (where we change starting pos of the enemies slightly)
            if event.type == obstacle_timer:
                random_number = random.randint(0, 1)

                if random_number:
                    obstacle_rectangle_list.append(human1_surface.get_rect
                                                   (midbottom=(random.randint(900, 1300), random.randint(390, 445))))
                else:
                    obstacle_rectangle_list.append(fly_surface.get_rect
                                                   (midbottom=(random.randint(900, 1300), random.randint(220, 270))))

            if event.type == human1_animation_timer:
                if human1_frame_index == 0 or human2_frame_index == 0:
                    human1_frame_index = 1
                    human2_frame_index = 1
                else:
                    human1_frame_index = 0
                    human2_frame_index = 0
                human1_surface = human1_frames[human1_frame_index]
                human2_surface = human2_frames[human2_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        # if game not active and user presses START or SPACE -> start game again
        else:
            if ((event.type == pygame.JOYBUTTONDOWN and event.button == 7)
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                is_game_active = True
                start_time = pygame.time.get_ticks()
