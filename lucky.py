# Module Importing
import pygame
from math import radians, sin, cos, sqrt
from random import randint, uniform
import sys

# pygame setup
screen_width = 1280
screen_height = 720

pygame.init()
pygame.font.init()
pygame.display.set_caption("shooting game (testing)")
screen = pygame.display.set_mode((screen_width, screen_height))
background = screen.copy()
default_font = pygame.font.Font(None, 72)


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    game()

        pygame.display.flip()


# Inside the game
def game():
    clock = pygame.time.Clock()

    dt = 0

    player_pos = pygame.Vector2(screen.get_width() // 2,
                                screen.get_height() // 2)
    player_size = 30
    player_spd = 300
    enemy_spd = 10
    rects = []
    lines = []
    lucky_block = []
    line_len = 75
    line_spd = 10
    time = 0
    status = 0
    status_rand = 0
    develop = True
    start_time = pygame.time.get_ticks()

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
        screen.blit(background, (0, 0))

        # Showing Timer
        current_time = pygame.time.get_ticks()
        elapsed_time = round((current_time - start_time) / 1000, 3)
        timer_text = default_font.render(f"Time: {elapsed_time}", True,
                                         (255, 255, 255))
        screen.blit(timer_text, (30, 30))

        if status > 0:
            enemy_spd = max(enemy_spd - 0.5, 5)
            line_spd = max(line_spd - 0.5, 5)
            # if 0 <= status_rand <= 25:
            #     player_spd = min(player_spd + 15, 500)
            # elif 25 <= status_rand <= 50:
            #     player_spd = max(player_spd - 15, 200)
            # elif 50 <= status_rand <= 75:
            #     player_size = min(player_size + 1, 45)
            # elif 75 <= status_rand <= 100:
            #     player_size = max(player_size - 1, 20)
        else:
            player_spd = max(player_spd - 10, 300)
            player_spd = min(player_spd + 10, 300)
            player_size = max(player_spd - 1, 30)
            player_size = min(player_spd + 1, 30)
            enemy_spd = min(enemy_spd + 0.5, 10)
            line_spd = min(line_spd + 0.5, 10)

        # Player properties
        pygame.draw.circle(screen, "white", player_pos, player_size)

        # Player Movements
        keys = pygame.key.get_pressed()

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
        # if keys[pygame.K_ESCAPE]:
        # UI design work, delay it first

        # Drawing Enemies
        for rect_pos, type, dir in rects:
            pygame.draw.rect(screen, "white",
                             (rect_pos.x - 20, rect_pos.y - 20, 40, 40))

        # Create bullet from enemy
        if time >= 180 and time % 45 == 0:
            for rect_pos, type, dir in rects:
                for deg in range(0, 360, 90):
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
                
                if develop:
                    continue
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

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button.collidepoint(mouse_pos):
                            game()

                    # Back to main screen
                    if keys[pygame.K_ESCAPE]:
                        main()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_button.collidepoint(mouse_pos):
                            main()

                    pygame.display.flip()

            # Moving the bullet
            line_pos.x += line_spd * cos(radians(line_bearing))
            line_pos.y -= line_spd * sin(radians(line_bearing))

            # Delete bullets / Out of screen
            if 0 <= line_pos.x <= screen_width and 0 <= line_pos.y <= screen_height:
                nxt_lines.append([line_pos.x, line_pos.y, line_bearing])

        lines = nxt_lines

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
            posx, posy = randint(0, screen_width), randint(0, screen_height)
            lucky_square = pygame.Rect(posx - 30, posy - 30, 60, 60)
            lucky_block.append(lucky_square)
        

        # Update Lucky Block
        lucky_block2 = []
        for lucky_square in lucky_block:
            if not lucky_square.collidepoint(player_pos):
                lucky_block2.append(lucky_square)
                dbwt(screen, lucky_square, "", default_font, "White", "Yellow")
            else :
                status = 150
                status_rand = uniform(0, 100)
        
        lucky_block = lucky_block2
        status -= 1

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.

        dt = clock.tick(60) / 1000
        time += 1  # time -> Number of loops


main()
pygame.quit()
