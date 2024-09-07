# Module Importing
import pygame
from math import radians, sin, cos, sqrt
from random import randint

# pygame setup
screen_width = 1280
screen_height = 720

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))

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


def main():

    clock = pygame.time.Clock()

    dt = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    rects = []
    lines = []
    line_len = 75
    line_spd = 10
    time = 0
    start_time = pygame.time.get_ticks()

    running = True

    while running:

        # Close Window Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background Color
        screen.fill("black")

        # Showing Timer
        current_time = pygame.time.get_ticks()
        elapsed_time = round((current_time - start_time) / 1000, 3)
        timer_text = default_font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        screen.blit(timer_text, (30, 30))
        
        # Player properties
        pygame.draw.circle(screen, "white", player_pos, 30)

        # Player Movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player_pos.y > 300 * dt + 30:
                player_pos.y -= 300 * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player_pos.x > 300 * dt + 30:
                player_pos.x -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if player_pos.y < screen_height - 300 * dt - 30:
                player_pos.y += 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player_pos.x < screen_width - 300 * dt - 30:
                player_pos.x += 300 * dt

        # Creating enemies
        while len(rects) < 3:
            rects.append(pygame.Vector2(randint(0, screen_width), randint(0, screen_height)))

        # Drawing Enemies
        for rect_pos in rects:
            pygame.draw.rect(screen, "white", (rect_pos.x - 20, rect_pos.y - 20, 40, 40))
        
        # Create bullet from enemy
        if time >= 180 and time % 45 == 0:
            for rect_pos in rects:
                for deg in range(0, 360, 45):
                    lines.append([rect_pos.x, rect_pos.y, deg])

        nxt_lines = []
        for line in lines:

            # Drawing bullets
            line_pos, line_bearing = pygame.Vector2(line[0], line[1]), line[2]
            end_pos = pygame.Vector2(line_pos.x + line_len * cos(radians(line_bearing)), line_pos.y - line_len * sin(radians(line_bearing)))
            pygame.draw.line(screen, "white", line_pos, end_pos, 5)

            # Check if collides
            if itlc(player_pos.x, player_pos.y, 30, line_pos.x, line_pos.y, end_pos.x, end_pos.y):
                restart_button = pygame.Rect(screen_width/2-150, screen_height/2-50, 300, 100)
                pygame.draw.rect(screen, "white", restart_button)

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                    
                    keys = pygame.key.get_pressed()
                    mouse_pos = pygame.mouse.get_pos()

                    # Button colour change when hover
                    if restart_button.collidepoint(mouse_pos):
                        dbwt(screen, restart_button, "Restart", default_font, "black", "gray69")
                    else:
                        dbwt(screen, restart_button, "Restart", default_font, "black", "white")


                    # Restart game
                    if keys[pygame.K_r]:
                        main()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button.collidepoint(mouse_pos):
                            main()
                    
                    pygame.display.flip()

            # Moving the bullet
            line_pos.x += line_spd * cos(radians(line_bearing))
            line_pos.y -= line_spd * sin(radians(line_bearing))

            # Delete bullets / Out of screen
            if 0 <= line_pos.x <= screen_width and 0 <= line_pos.y <= screen_height:
                nxt_lines.append([line_pos.x, line_pos.y, line_bearing])
        
        lines = nxt_lines

        for rect_pos in rects:

            # Enemy random movement
            rect_dx = randint(-1, 1) * 5
            rect_dy = randint(-1, 1) * 5

            # Set Boundaries for the enemy
            if 0 <= rect_pos.x + rect_dx <= screen_width:
                rect_pos.x += rect_dx
            if 0 <= rect_pos.y + rect_dy <= screen_height:
                rect_pos.y += rect_dy

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.

        dt = clock.tick(60) / 1000
        time += 1 # time -> Number of loops

main()
pygame.quit()