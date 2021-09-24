import pygame
import sys


def draw_floor(x_floor):
    screen.blit(floor, (x_floor, y_floor))
    x_floor = x_floor + x_screen
    screen.blit(floor, (x_floor, y_floor))


pygame.init()

x_screen = 216
y_screen = 384
screen = pygame.display.set_mode((x_screen, y_screen))

# Set fps 
clock = pygame.time.Clock()
fps_number = 90

# O(0,0)
Ox = 0
Oy = 0

# Set background
background = pygame.image.load('./assests/background-night.png').convert()
x_background = Ox
y_background = Oy
# background = pygame.transform.scale2x(background)

# Set floor
floor = pygame.image.load('./assests/floor.png').convert()
# floor =pygame.transform.scale2x(floor)
x_floor = Ox
# y_floor < x_screen
y_floor = 300


# Set bird
# Convert have pygame load img faster 
bird = pygame.image.load('./assests/yellowbird-midflap.png').convert()
x_bird = x_screen / 3
y_bird = y_screen / 2 
bird_rect = bird.get_rect(center=(x_bird, y_bird))


# Create gravity
gravity = 0.25
# Bird not move yet
bird_movement = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -8

    # Draw background
    screen.blit(background, (x_background, y_background))

    # Draw floor
    x_floor -= 1
    draw_floor(x_floor)
    if x_floor <= -x_screen:
        x_floor = Ox

    # Draw bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird, bird_rect)

    pygame.display.update()
    clock.tick(fps_number)
