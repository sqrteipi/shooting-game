# Example file showing a circle moving on screen
import pygame
from math import radians, sin, cos

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
rect_pos = pygame.Vector2(1280 * 3 / 4, 720 / 2)
lines = []
line_len = 75
line_spd = 10
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # player properties
    pygame.draw.circle(screen, "white", player_pos, 30)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # enemy properties
    pygame.draw.rect(screen, "white", (rect_pos.x - 20, rect_pos.y - 20, 40, 40))
    
    if time >= 100 and time % 50 == 0:
        for deg in range(0, 360, 45):
            lines.append([rect_pos.x, rect_pos.y, deg])

    nxt_lines = []
    for line in lines:
        line_pos, line_bearing = pygame.Vector2(line[0], line[1]), line[2]
        end_pos = (line_pos.x + line_len * cos(radians(line_bearing)), line_pos.y - line_len * sin(radians(line_bearing)))
        pygame.draw.line(screen, "white", line_pos, end_pos, 5)
        line_pos.x += line_spd * cos(radians(line_bearing))
        line_pos.y -= line_spd * sin(radians(line_bearing))
        if line_pos.x >= 0 and line_pos.x <= 1280 and line_pos.y >= 0 and line_pos.y <= 720:
            nxt_lines.append([line_pos.x, line_pos.y, line_bearing])
    
    lines = nxt_lines

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    time += 1

pygame.quit()