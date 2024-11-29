# Module Importing
import pygame
from math import *
from random import randint, uniform
import sys

# pygame setup

pygame.init()
pygame.font.init()
pygame.display.set_caption("shooting game (testing)")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen_width, screen_height = screen.get_size()
print(screen_width, screen_height)

t_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

default_font = pygame.font.Font(None, 65)

debug_mode = False # Not die

# Check if a line intersects with a circle
def itlc(x0, y0, r, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    a = dx**2 + dy**2
    b = 2 * (dx * (x1 - x0) + dy * (y1 - y0))
    c = (x1 - x0)**2 + (y1 - y0)**2 - r**2

    D = b**2 - 4 * a * c

    if D < 0:
        return False

    sqrtD = sqrt(D)
    t1 = (-b - sqrtD) / (2 * a)
    t2 = (-b + sqrtD) / (2 * a)

    if (0 <= t1 <= 1) or (0 <= t2 <= 1):
        return True
    return False

# Drawing button with text
def dbwt(screen, button_rect, text, font, text_color, button_color):
    pygame.draw.rect(screen, button_color, button_rect)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# Showing Timer
def show_info(start_time, score):
    info_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    info_screen.fill((0, 0, 0, 255))
    current_time = pygame.time.get_ticks()
    elapsed_time = round((current_time - start_time) / 1000, 3)
    timer_text = default_font.render(f"Time: {elapsed_time}", True, (128, 128, 128, 128))
    info_screen.blit(timer_text, (30, 30))

    score = round(elapsed_time * 25 + score * 250)
    score_text = default_font.render(f"Score: {score}", True, (128, 128, 128, 128))
    info_screen.blit(score_text, (30, 80))

    screen.blit(info_screen, (0, 0))

# Main screen
def main():

    # Start button
    screen.fill("black")
    start_button = pygame.Rect(screen_width * 0.4, screen_height * 0.45, screen_width * 0.2, screen_height * 0.1)
    pygame.draw.rect(screen, "white", start_button)
    dbwt(screen, start_button, "Start Game", default_font, "black", "white")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            # Button colour change when hover
            if start_button.collidepoint(mouse_pos):
                dbwt(screen, start_button, "Start Game", default_font, "black",
                     "gray69")
            else:
                dbwt(screen, start_button, "Start Game", default_font, "black",
                     "white")

            # Start game
            if keys[pygame.K_RETURN]:
                htp()
            
            if keys[pygame.K_ESCAPE]:
                sys.exit()

            if mouse_click[0]:
                if start_button.collidepoint(mouse_pos):
                    htp()

        pygame.display.flip()

# Restart Screen
def restart(start_time, score):

    if debug_mode == True:
        return

    screen.fill("black")
    show_info(start_time, score)

    # Restart Button
    restart_button = pygame.Rect(screen_width * 0.4, screen_height * 0.35, screen_width * 0.2, screen_height * 0.1)
    back_button = pygame.Rect(screen_width * 0.4, screen_height * 0.55, screen_width * 0.2, screen_height * 0.1)

    dbwt(screen, restart_button, "Restart", default_font, "black",
        "white")
    dbwt(screen, back_button, "Back to menu", default_font,
        "black", "white")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Button colour change when hover
        if restart_button.collidepoint(mouse_pos):
            dbwt(screen, restart_button, "Restart", default_font,
                "black", "gray69")
        else:
            dbwt(screen, restart_button, "Restart", default_font,
                "black", "white")

        if back_button.collidepoint(mouse_pos):
            dbwt(screen, back_button, "Back to menu", default_font,
                "black", "gray69")
        else:
            dbwt(screen, back_button, "Back to menu", default_font,
                "black", "white")

        # Restart game
        if keys[pygame.K_r]:
            game()

        if mouse_click[0]:
            if restart_button.collidepoint(mouse_pos):
                game()

        # Back to main screen
        if keys[pygame.K_ESCAPE]:
            main()

        if mouse_click[0]:
            if back_button.collidepoint(mouse_pos):
                main()

        pygame.display.flip()

# How to play
def htp():

    screen.fill("black")
    how_to_play_text = pygame.Rect(screen_width * 0.3, screen_height * 0.1, screen_width * 0.4, screen_height * 0.1)
    how_to_play_text_2 = pygame.Rect(screen_width * 0.3, screen_height * 0.2, screen_width * 0.4, screen_height * 0.1)
    dbwt(screen, how_to_play_text, "Use arrow keys or WASD to control.", default_font, "white", "black")
    dbwt(screen, how_to_play_text_2, "Avoid any bullets or x-rays.", default_font, "white", "black")
    start_button = pygame.Rect(screen_width * 0.4, screen_height * 0.45, screen_width * 0.2, screen_height * 0.1)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.draw.rect(screen, "white", start_button)
    dbwt(screen, start_button, "Start Game", default_font, "black", "white")

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            keys = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if keys[pygame.K_ESCAPE]:
                sys.exit()

            # Button colour change when hover
            if start_button.collidepoint(mouse_pos):
                dbwt(screen, start_button, "Start Game", default_font, "black",
                     "gray69")
            else:
                dbwt(screen, start_button, "Start Game", default_font, "black",
                     "white")

            # Start game
            if keys[pygame.K_RETURN]:
                game()

            if mouse_click[0]:
                if start_button.collidepoint(mouse_pos):
                    game()

        pygame.display.flip()

# Inside the game
def game():

    screen.fill("black")

    clock = pygame.time.Clock()

    # Time
    dt = 0
    time = 0
    score = 0

    # Player
    player_pos = pygame.Vector2(screen.get_width() // 2,
                                screen.get_height() // 2)
    player_size = screen_width * 0.02
    initial_player_size = player_size
    player_spd = screen_width * 0.3
    initial_player_spd = player_spd

    # Objects
    rects = []
    lines = []
    t_lines = []
    lucky_block = []

    # Bullets
    line_len = screen_width * 0.06
    line_spd = screen_width * 0.005
    initial_line_spd = line_spd
    bullet_reload = 60
    bullet_amount = 3
    xray_chance = 5

    enemy_size = screen_width * 0.025
    lucky_block_size = screen_width * 0.04

    enemy_spd = screen_width * 0.007
    initial_enemy_spd = enemy_spd

    status = 0

    # Creating enemies
    rects.append([
        pygame.Vector2(randint(0, screen_width), randint(0, screen_height)), 0,
        uniform(0, 360)
    ])

    # Countdown

    pygame.draw.circle(screen, "white", player_pos, player_size)
    for rect_pos, type, dir in rects:
        pygame.draw.rect(screen, "white", (rect_pos.x - 20, rect_pos.y - 20, enemy_size, enemy_size))
    start_text_block = pygame.Rect(screen_width // 2 - 100, 50, 200, 200)
    dbwt(screen, start_text_block, "3.", default_font, "white", "black")
    pygame.display.flip()
    pygame.time.delay(1000)
    dbwt(screen, start_text_block, "2..", default_font, "white", "black")
    pygame.display.flip()
    pygame.time.delay(1000)
    dbwt(screen, start_text_block, "1...", default_font, "white", "black")
    pygame.display.flip()
    pygame.time.delay(1000) 

    start_time = pygame.time.get_ticks()
    
    running = True

    while running:

        # Close Window Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        # Background Color
        screen.fill("black")

        # Showing Timer
        show_info(start_time, score)

        # Updating Status
        if status > 0:
            if 1 <= status_rand <= 1:
                player_spd = min(player_spd + 15, initial_player_spd * 1.2)
            elif 2 <= status_rand <= 2:
                player_spd = max(player_spd - 15, initial_player_spd * 0.8)
            elif 3 <= status_rand <= 3:
                player_size = min(player_size + 1, initial_player_size * 1.2)
            elif 4 <= status_rand <= 4:
                player_size = max(player_size - 1, initial_player_size * 0.8)
            elif 5 <= status_rand <= 5:
                enemy_spd = max(enemy_spd - 0.5, initial_enemy_spd * 0.5)
                line_spd = max(line_spd - 0.5, initial_line_spd * 0.5)
        else:
            player_spd = max(player_spd - 10, initial_player_spd)
            player_spd = min(player_spd + 10, initial_player_spd)
            player_size = max(player_size - 1, initial_player_size)
            player_size = min(player_size + 1, initial_player_size)
            enemy_spd = min(enemy_spd + 0.5, initial_enemy_spd)
            line_spd = min(line_spd + 0.5, initial_line_spd)
        
        # Player properties
        pygame.draw.circle(screen, "white", player_pos, player_size)

        # Player Movements
        keys = pygame.key.get_pressed()

        if time > 5:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if player_pos.y > player_spd * dt + player_size:
                    player_pos.y -= player_spd * dt

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if player_pos.x > player_spd * dt + player_size:
                    player_pos.x -= player_spd * dt

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if player_pos.y < screen_height - player_spd * dt - player_size:
                    player_pos.y += player_spd * dt

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if player_pos.x < screen_width - player_spd * dt - player_size:
                    player_pos.x += player_spd * dt

        # In-game options menu
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        # UI design work, delay it first

        # Drawing Enemies
        for rect_pos, type, dir in rects:
            pygame.draw.rect(screen, "white",
                             (rect_pos.x - enemy_size // 2, rect_pos.y - enemy_size // 2, enemy_size, enemy_size))

        # Create bullet from enemy
        if time >= 180 and time % bullet_reload == 0:
            for rect_pos, type, dir in rects:
                for i in range(bullet_amount):
                    deg = 360/bullet_amount*i
                    lines.append([rect_pos.x, rect_pos.y, deg])

        nxt_lines = []
        for line in lines:

            # Drawing bullets
            line_pos, line_bearing = pygame.Vector2(line[0], line[1]), line[2]
            end_pos = pygame.Vector2(
                line_pos.x + line_len * cos(radians(line_bearing)),
                line_pos.y - line_len * sin(radians(line_bearing)))
            pygame.draw.line(screen, "white", line_pos, end_pos, 5)

            # Check if collides
            if itlc(player_pos.x, player_pos.y, player_size, line_pos.x,
                    line_pos.y, end_pos.x, end_pos.y):
                restart(start_time, score)

            # Moving the bullets
            line_pos.x += line_spd * cos(radians(line_bearing))
            line_pos.y -= line_spd * sin(radians(line_bearing))

            # Delete bullets / Out of screen
            if 0 <= line_pos.x <= screen_width and 0 <= line_pos.y <= screen_height:
                nxt_lines.append([line_pos.x, line_pos.y, line_bearing])

        lines = nxt_lines

        # Attack Screen Initialize
        t_screen.fill((0, 0, 0, 0))
        # screen.blit(t_screen, (0, 0))

        # Drawing X-Rays
        for t_line in t_lines:
            if t_line[4] > time:
                pygame.draw.line(t_screen, (255, 255, 255, 128),
                                 [t_line[0], t_line[1]],
                                 [t_line[2], t_line[3]], 5)
            elif t_line[4] > time - 20:
                pygame.draw.line(t_screen, (255, 255, 255, 255),
                                 [t_line[0], t_line[1]],
                                 [t_line[2], t_line[3]], 5)
                # pygame.display.flip()
                if itlc(player_pos.x, player_pos.y, player_size, t_line[0], t_line[1], t_line[2], t_line[3]):
                    pygame.display.flip()
                    restart(start_time, score)
            else:
                pygame.draw.line(t_screen, (255, 255, 255, 0),
                                 [t_line[0], t_line[1]],
                                 [t_line[2], t_line[3]], 5)
                t_lines.remove(t_line)

        # Random - X-Ray
        xray_random = uniform(0, 1000)
        if xray_random <= xray_chance and time > 180:
            if xray_random < xray_chance/2:
                t_lines.append([
                    0,
                    round(uniform(0, screen_height)), screen_width,
                    round(uniform(0, screen_height)),
                    time + round(uniform(40, 80))
                ])
            else:
                t_lines.append([
                    round(uniform(0, screen_width)), 0,
                    round(uniform(0, screen_width)), screen_height,
                    time + round(uniform(40, 80))
                ])

        screen.blit(t_screen, (0, 0))

        # Moving Enemies
        nxt_rects = []
        for rect_pos, type, dir in rects:
            rect_dx = cos(radians(dir)) * enemy_spd
            rect_dy = sin(radians(dir)) * enemy_spd

            # Set Boundaries for the enemy
            while not (0 <= rect_pos.x + rect_dx <= screen_width
                       and 0 <= rect_pos.y + rect_dy <= screen_height):
                dir = uniform(0, 360)
                rect_dx = cos(radians(dir)) * enemy_spd
                rect_dy = sin(radians(dir)) * enemy_spd

            rect_pos.x += rect_dx
            rect_pos.y += rect_dy
            nxt_rects.append([rect_pos, type, dir])

        rects = nxt_rects
        
        # Create Lucky Block
        if len(lucky_block) == 0 and status == -150:
            posx, posy = randint(30, screen_width - 30), randint(30, screen_height - 30)
            lucky_square = pygame.Rect(posx - lucky_block_size // 2, posy - lucky_block_size // 2, lucky_block_size, lucky_block_size)
            lucky_block.append(lucky_square)


        # Update Lucky Block
        lucky_block2 = []
        for lucky_square in lucky_block:
            if not lucky_square.collidepoint(player_pos):
                lucky_block2.append(lucky_square)
                dbwt(screen, lucky_square, "", default_font, "White", "Yellow")
            else :
                # Touched Lucky Block
                status = 150
                status_rand = randint(1, 5)
                score += 1

        lucky_block = lucky_block2
        status -= 1

        # Bullets stats changing

        if bullet_amount >= 4 and time > 0 and time % 1000 == 500:
            if bullet_amount < 8:
                bullet_amount += 1
            if bullet_reload > 10:
                bullet_reload = ceil(bullet_reload * 0.9)
            if line_spd < 25:
                line_spd = ceil(line_spd*1.1)
            if xray_chance < 75:
                xray_chance *= 1.1
        
        if bullet_amount < 4 and time > 0 and time % 500 == 0:
            bullet_amount += 1
        


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        time += 1  # time -> Number of loops


main()

