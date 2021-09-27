import pygame
import sys
import random


class World:
    def __init__(self):
        self.gravity = 0.25


def draw_back_ground():
    # Set background location
    x_background = 0
    y_background = 0
    screen.blit(background_img, (x_background, y_background))


def draw_floor(x_floor):
    screen.blit(floor_img, (x_floor, y_floor))
    x_floor += SCREEN_WIDTH
    screen.blit(floor_img, (x_floor, y_floor))


class BIRD(pygame.sprite.Sprite):
    def __init__(self, image):
        # Set bird location
        x_bird = SCREEN_WIDTH / 3
        y_bird = SCREEN_HEIGHT / 2
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x_bird, y_bird))
        self.bird_movement = 0

    def draw_bird(self):
        self.move_bird()
        screen.blit(self.image, self.rect)

    def move_bird(self):
        self.bird_movement += world.gravity
        self.rect.centery += self.bird_movement
        return self.rect


class PIPE(pygame.sprite.Sprite):
    def __init__(self, image):
        random_pipe_pos = random.choice(pipe_height)
        x_pipe = SCREEN_WIDTH
        y_pipe = random_pipe_pos
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.bottom_pipe = self.image.get_rect(midtop=(x_pipe, y_pipe))
        self.top_pipe = self.image.get_rect(midtop=(x_pipe, y_pipe - SCREEN_HEIGHT))


pygame.init()
# Set screen
SCREEN_WIDTH = 216
SCREEN_HEIGHT = 384
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set fps
clock = pygame.time.Clock()
fps_number = 90

# Load image
background_img = pygame.image.load('./assests/background-night.png').convert_alpha()
floor_img = pygame.image.load('./assests/floor.png').convert_alpha()
bird_down = pygame.image.load('./assests/yellowbird-downflap.png').convert()
bird_up = pygame.image.load('./assests/yellowbird-upflap.png').convert()
bird_mid = pygame.image.load('./assests/yellowbird-midflap.png').convert()
pipe_img = pygame.image.load('./assests/pipe-green.png').convert()

# List bird
bird_list = [bird_mid]
bird_index = 0
bird = bird_list[bird_index]

pipe_height = [SCREEN_HEIGHT/2, SCREEN_HEIGHT / 1.5]


# Set floor location
x_floor = 0
y_floor = SCREEN_HEIGHT * 0.75

# Object init
world = World()
bird = BIRD(bird)
pipe = PIPE(pipe_img)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.bird_movement = -5

    # Draw background
    draw_back_ground()

    # Draw floor
    x_floor -= 1
    draw_floor(x_floor)
    if x_floor <= -SCREEN_WIDTH:
        x_floor = 0

    # Draw bird
    bird.draw_bird()

    # Draw pipe
    # pipe.draw_pipe()

    pygame.display.update()
    clock.tick(fps_number)
