import pygame
import sys
import random


def draw_floor(x_floor):
    screen.blit(floor, (x_floor, y_floor))
    x_floor = x_floor + x_screen
    screen.blit(floor, (x_floor, y_floor))


def create_bird():
    x_bird = x_screen / 3
    y_bird = y_screen / 2
    bird_rect = bird.get_rect(center=(x_bird, y_bird))
    return bird_rect


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    x_pipe = x_screen
    y_pipe = random_pipe_pos
    bottom_pipe = pipe_surface.get_rect(midtop=(x_pipe, y_pipe))
    top_pipe = pipe_surface.get_rect(midtop=(x_pipe, y_pipe - 400))
    return bottom_pipe,top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)


pygame.init()


# Set screen
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
bird_rect = create_bird()


# Create gravity
gravity = 0.25
# Bird not move yet
bird_movement = 0


# Create pipe
pipe_surface = pygame.image.load('./assests/pipe-green.png').convert()
pipe_list = []


# Create timer
spawnpipe = pygame.USEREVENT
# New pipe will appear in every 1200 ms
spawnpipe_time = 1200
pygame.time.set_timer(spawnpipe, spawnpipe_time)
pipe_height = [y_screen/2, y_screen/3, y_screen / 1.5]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = -6
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    # Draw background
    screen.blit(background, (x_background, y_background))

    # Draw floor
    x_floor -= 1
    draw_floor(x_floor)
    if x_floor <= -x_screen:
        x_floor = Ox

    # Draw pipes
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)

    # Draw bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird, bird_rect)

    pygame.display.update()
    clock.tick(fps_number)
