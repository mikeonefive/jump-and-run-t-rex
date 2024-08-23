import pygame
import sys
import random

from player import Player
from enemy import Enemy
from moving_items import MovingItems

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


def check_collisions():
    # True/False here deletes or doesn't delete the enemy sprite
    if pygame.sprite.spritecollide(player.sprite, enemy_group, False):
        enemy_group.empty()     # delete all sprites in group because would trigger more collisions
        item_group.empty()
        return False
    else:
        return True


def animate_background():
    global background_scroll

    # endless background scroll
    background_scroll -= 4  # moving to left with every while loop iteration
    # if off screen -get_width() put next image at pos 0
    if background_scroll <= - ground_surface.get_width():
        background_scroll = 0

    screen.blit(graywall_surface, (background_scroll, 0))
    screen.blit(graywall_surface, (graywall_surface.get_width() + background_scroll, 0))

    screen.blit(wall_surface, (background_scroll, 0))
    screen.blit(wall_surface, (wall_surface.get_width() + background_scroll, 0))

    screen.blit(ground_surface, (background_scroll, 0))
    screen.blit(ground_surface, (ground_surface.get_width() + background_scroll, 0))


# initializes pygame, initiates all the things (images, sounds) we need
pygame.init()
pygame.joystick.init()

# store joysticks in list
joysticks = []

# SCREEN & CLOCK
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump and run and jump and run, T-Rex!")
clock = pygame.time.Clock()     # clock for the framerate
is_game_active = False
start_time = 0
score = 0
background_scroll = 0
background_music = pygame.mixer.Sound("sounds/music.wav")
background_music.play(loops=-1)

# GROUPS/SPRITES
player = pygame.sprite.GroupSingle()
player.sprite = Player(joysticks)       # pass in joysticks list as parameter so it can be used in both player and game

enemy_group = pygame.sprite.Group()

item_group = pygame.sprite.Group()

# BACKGROUND SURFACES & ITEM SURFACES
sky_surface = pygame.image.load("assets/backgrounds/sky.png").convert_alpha()
buildings_surface = pygame.image.load("assets/backgrounds/buildings.png").convert_alpha()
graywall_surface = pygame.image.load("assets/backgrounds/graywall.png").convert_alpha()
wall_surface = pygame.image.load("assets/backgrounds/cleanwall.png").convert_alpha()
graffitiwall_surface = pygame.image.load("assets/backgrounds/graffitiwall.png").convert_alpha()
ground_surface = pygame.image.load("assets/backgrounds/ground.png").convert_alpha()

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

# BACKGROUND TIMER (let houses and items appear at random intervals)
background_timer = pygame.USEREVENT + 2
pygame.time.set_timer(background_timer, random.randint(4000, 6000))

is_main_loop_running = True
# MAIN GAME LOOP, entire game runs in this loop
while is_main_loop_running:

    if is_game_active:
        # draw background and score
        screen.blit(sky_surface, (0, 0))   # blit puts 1 surface on another, order matters (background first)
        screen.blit(buildings_surface, (0, 0))

        animate_background()

        score = display_time_and_calculate_score()

        item_group.draw(screen)
        item_group.update()

        enemy_group.draw(screen)
        enemy_group.update()

        player.draw(screen)
        player.update()

        # COLLISIONS
        is_game_active = check_collisions()

    # GAME OVER SCREEN if current game not active
    else:
        screen.fill("black")
        screen.blit(player_gameover_scaled, player_gameover_rectangle)
        player.sprite.rect.midbottom = (100, 400)  # put player back to original start pos (e.g. jumping at gameover)
        player.gravity = 0

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
        # if game window is closed quit the game
        if event.type == pygame.QUIT:
            is_main_loop_running = False
            pygame.quit()
            sys.exit()  # need to exit here because otherwise pygame.display.update() would cause an error

        # if joystick is plugged in, add it to the joysticks list
        if event.type == pygame.JOYDEVICEADDED:
            joysticks.append(pygame.joystick.Joystick(event.device_index))

        if is_game_active:
            # ENEMIES/OBSTACLES intervals
            if event.type == obstacle_timer:
                random_enemy = Enemy(random.choice(["fly", "human1", "human2", "human1", "human2"]))
                enemy_group.add(random_enemy)

            if event.type == background_timer:
                random_item = MovingItems(random.choice(["house", "streetlights", "boxes", "hydrant", "bottle",
                                                         "tires"]))
                item_group.add(random_item)

        # if game not active and user presses START or SPACE -> start game again
        else:
            if ((event.type == pygame.JOYBUTTONDOWN and event.button == 7)
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                is_game_active = True
                start_time = pygame.time.get_ticks()
