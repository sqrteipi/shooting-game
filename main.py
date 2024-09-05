# Module Importing
import pygame
from math import radians, sin, cos, sqrt
from random import randint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
rects = []
lines = []
line_len = 75
line_spd = 10
time = 0

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
    while len(rects) < 3:
        rects.append(pygame.Vector2(randint(0, 1280), randint(0, 720)))

    for rect_pos in rects:
        pygame.draw.rect(screen, "white", (rect_pos.x - 20, rect_pos.y - 20, 40, 40))
    
    if time >= 80 and time % 40 == 0:
        for rect_pos in rects:
            for deg in range(0, 360, 45):
                lines.append([rect_pos.x, rect_pos.y, deg])

    nxt_lines = []
    for line in lines:
        line_pos, line_bearing = pygame.Vector2(line[0], line[1]), line[2]
        end_pos = pygame.Vector2(line_pos.x + line_len * cos(radians(line_bearing)), line_pos.y - line_len * sin(radians(line_bearing)))
        pygame.draw.line(screen, "white", line_pos, end_pos, 5)

        if itlc(player_pos.x, player_pos.y, 30, line_pos.x, line_pos.y, end_pos.x, end_pos.y):
            running = False

        line_pos.x += line_spd * cos(radians(line_bearing))
        line_pos.y -= line_spd * sin(radians(line_bearing))

        if 0 <= line_pos.x <= 1280 and 0 <= line_pos.y <= 720:
            nxt_lines.append([line_pos.x, line_pos.y, line_bearing])
    
    lines = nxt_lines

    for rect_pos in rects:
        rect_dx = randint(-3, 3) * 7
        rect_dy = randint(-3, 3) * 7

        if 0 <= rect_pos.x + rect_dx <= 1280:
            rect_pos.x += rect_dx
        if 0 <= rect_pos.y + rect_dy <= 720:
            rect_pos.y += rect_dy

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    time += 1

pygame.quit()