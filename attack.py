# Module Importing
import pygame
from math import *
from random import randint, uniform
import sys

# pygame setup
screen_width = 1280
screen_height = 720
pygame.init()
pygame.font.init()
pygame.display.set_caption("shooting game (testing)")
screen = pygame.display.set_mode((screen_width, screen_height))
t_screen = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

default_font = pygame.font.Font(None, 72)

debug_mode = False


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

def show_timer(start_time):
    current_time = pygame.time.get_ticks()
    elapsed_time = round((current_time - start_time) / 1000, 3)
    timer_text = default_font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
    screen.blit(timer_text, (30, 30))

# Main screen
def main():

    # Start button
    screen.fill("black")
    start_button = pygame.Rect(screen_width // 2 - 200,
                               screen_height // 2 - 50, 400, 100)
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
                game()
            
            if keys[pygame.K_ESCAPE]:
                sys.exit()

            if mouse_click[0]:
                if start_button.collidepoint(mouse_pos):
                    game()

        pygame.display.flip()


def restart(start_time):

    if debug_mode == True:
        return

    screen.fill("black")
    show_timer(start_time)

    # Restart Button
    restart_button = pygame.Rect(screen_width // 2 - 200,
                                screen_height // 2 - 150, 400,
                                100)
    back_button = pygame.Rect(screen_width // 2 - 200,
                            screen_height // 2 + 50, 400, 100)

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


# Inside the game
def game():

    clock = pygame.time.Clock()

    dt = 0
    time = 0
    player_pos = pygame.Vector2(screen.get_width() // 2,
                                screen.get_height() // 2)
    player_size = 30
    rects = []
    lines = []
    t_lines = []
    bubbles = []
    line_len = 75
    line_spd = 10
    start_time = pygame.time.get_ticks()
    bullet_reload = 45
    bullet_amount = 4
    xray_chance = 10
    bubble_chance = 10

    # Creating enemies
    rects.append([
        pygame.Vector2(randint(0, screen_width), randint(0, screen_height)), 0,
        uniform(0, 360)
    ])

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
        show_timer(start_time)

        # Player properties
        pygame.draw.circle(screen, "white", player_pos, player_size)

        # Player Movements
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player_pos.y > 300 * dt + player_size:
                player_pos.y -= 300 * dt

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player_pos.x > 300 * dt + player_size:
                player_pos.x -= 300 * dt

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player_pos.y < screen_height - 300 * dt - player_size:
                player_pos.y += 300 * dt

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player_pos.x < screen_width - 300 * dt - player_size:
                player_pos.x += 300 * dt

        # In-game options menu
        # if keys[pygame.K_ESCAPE]:
        # UI design work, delay it first

        # Drawing Enemies
        for rect_pos, type, dir in rects:
            pygame.draw.rect(screen, "white",
                             (rect_pos.x - 20, rect_pos.y - 20, 40, 40))

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
                    line_pos.y, end_pos.x, end_pos.y) and time < 0:
                
                restart(start_time)

            # Moving the bullet
            line_pos.x += line_spd * cos(radians(line_bearing))
            line_pos.y -= line_spd * sin(radians(line_bearing))

            # Delete bullets / Out of screen
            if 0 <= line_pos.x <= screen_width and 0 <= line_pos.y <= screen_height:
                nxt_lines.append([line_pos.x, line_pos.y, line_bearing])

        lines = nxt_lines

        # Attack Screen Initialize
        t_screen.fill((0, 0, 0, 0))
        screen.blit(t_screen, (0, 0))

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
                pygame.display.flip()
                if itlc(player_pos.x, player_pos.y, player_size, t_line[0], t_line[1], t_line[2], t_line[3]):
                    pygame.display.flip()
                    restart(start_time)
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

        # Drawing Bubblers
        for bubble in bubbles:
            if bubble[3] > time:
                pygame.draw.rect(t_screen, (255, 255, 255, 128), (bubble[0], bubble[1], bubble[2], bubble[2]))
            elif bubble[3] > time-60:
                pygame.draw.rect(t_screen, (255, 255, 255, 255), (bubble[0], bubble[1], bubble[2], bubble[2]))
            else:
                pygame.draw.rect(t_screen, (255, 255, 255, 0), (bubble[0], bubble[1], bubble[2], bubble[2]))
                bubbles.remove(bubble)

        # Random - Bubbler
        bubble_random = uniform(0, 1000)
        if bubble_random <= bubble_chance and time > 180:
            bubbles.append([round(uniform(0, screen_width-70)), round(uniform(0, screen_height-70)), round(uniform(30, 70)), time+round(uniform(25, 50))])

        nxt_rects = []
        for rect_pos, type, dir in rects:
            rect_dx = cos(radians(dir)) * 10
            rect_dy = sin(radians(dir)) * 10

            # Set Boundaries for the enemy
            while not (0 <= rect_pos.x + rect_dx <= screen_width
                       and 0 <= rect_pos.y + rect_dy <= screen_height):
                dir = uniform(0, 360)
                rect_dx = cos(radians(dir)) * 10
                rect_dy = sin(radians(dir)) * 10

            rect_pos.x += rect_dx
            rect_pos.y += rect_dy
            nxt_rects.append([rect_pos, type, dir])

        rects = nxt_rects
        screen.blit(t_screen, (0, 0))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.

        # Bullets stats changing
        if time > 0 and time % 1000 == 0:
            if bullet_amount < 16:
                bullet_amount += 1
            if bullet_reload > 10:
                bullet_reload = ceil(bullet_reload*0.9)
            if line_spd < 25:
                line_spd = ceil(line_spd*1.1)
            if xray_chance < 75:
                xray_chance *= 1.1
            if bubble_chance < 75:
                bubble_chance *= 1.1

        dt = clock.tick(60) / 1000
        time += 1  # time -> Number of loops


main()
pygame.quit()
