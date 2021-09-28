import pygame
import sys
import random


class World:
    def __init__(self):
        self.gravity = 0.25
        # Set fps
        self.clock = pygame.time.Clock()
        self.fps_number = 90
        # Set floor location
        self.x_floor = 0
        self.y_floor = SCREEN_HEIGHT * 0.75
        # Game status
        self.game_active = True

    def draw_back_ground(self):
        # Set background location
        x_background = 0
        y_background = 0
        screen.blit(background_img, (x_background, y_background))

    def draw_floor(self, x_floor):
        screen.blit(floor_img, (x_floor, self.y_floor))
        x_floor += SCREEN_WIDTH
        screen.blit(floor_img, (x_floor, self.y_floor))


class BIRD(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        # Set bird location
        self.x_bird = SCREEN_WIDTH / 3
        self.y_bird = SCREEN_HEIGHT / 2
        self.image = image
        self.rect = self.image.get_rect(center=(self.x_bird, self.y_bird))
        self.bird_movement = 0

    def draw_bird(self):
        self.move_bird()
        screen.blit(self.image, self.rect)

    def move_bird(self):
        self.bird_movement += world.gravity
        self.rect.centery += self.bird_movement
        return self.rect

    def check_collision(self, pipes):
        for pipe in pipes:
            if self.rect.colliderect(pipe):
                # hit_sound.play()
                return False
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            # hit_sound.play()
            return False
        return True


class PIPE(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        self.pipe_height = [SCREEN_HEIGHT/2, SCREEN_HEIGHT/1.5, SCREEN_HEIGHT/3]
        random_pipe_pos = random.choice(self.pipe_height)
        x_pipe = SCREEN_WIDTH
        y_pipe = random_pipe_pos

        self.image = image
        self.bottom_pipe = self.image.get_rect(midtop=(x_pipe, y_pipe))
        self.top_pipe = self.image.get_rect(midtop=(x_pipe, y_pipe - SCREEN_HEIGHT))
        self.pipe_list = []

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        x_pipe = SCREEN_WIDTH
        y_pipe = random_pipe_pos
        bottom_pipe = pipe_img.get_rect(midtop=(x_pipe, y_pipe))
        top_pipe = pipe_img.get_rect(midtop=(x_pipe, y_pipe - SCREEN_HEIGHT))
        return bottom_pipe, top_pipe

    def move_pipe(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 2
        return pipes

    def draw_pipe(self, pipes):
        pipes = self.move_pipe(pipes)
        for pipe in pipes:
            if pipe.bottom >= SCREEN_HEIGHT * (9 / 10):
                screen.blit(pipe_img, pipe)
            else:
                # Only flip y_axis
                flip_pipe = pygame.transform.flip(pipe_img, False, True)
                screen.blit(flip_pipe, pipe)


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    return image


pygame.init()
# Set screen
SCREEN_WIDTH = 216
SCREEN_HEIGHT = 384
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Load image
background_img = load_image('./assests/background-night.png')
floor_img = load_image('./assests/floor.png')
bird_down = load_image('./assests/yellowbird-downflap.png')
bird_up = load_image('./assests/yellowbird-upflap.png')
bird_mid = load_image('./assests/yellowbird-midflap.png')
pipe_img = load_image('./assests/pipe-green.png')

# List bird
bird_list = [bird_mid]
bird_index = 0
bird = bird_list[bird_index]


# Object init
world = World()
bird = BIRD(bird)
pipe = PIPE(pipe_img)
pipe_list = pipe.pipe_list

# Set timer for pipe
spawn_pipe = pygame.USEREVENT
spawn_pipe_time = 1200
pygame.time.set_timer(spawn_pipe, spawn_pipe_time)

# Set x_floor
x_floor = world.x_floor

game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird.bird_movement = -5
                # Play again
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                # reset pipe list
                pipe_list.clear()
                bird.rect.center = (bird.x_bird, bird.y_bird)
                bird.bird_movement = 0
        if event.type == spawn_pipe:
            pipe_list.extend(pipe.create_pipe())

    # Draw background
    world.draw_back_ground()

    # Draw floor
    x_floor -= 1
    world.draw_floor(x_floor)
    if x_floor <= -SCREEN_WIDTH:
        x_floor = 0

    if world.game_active:

        # Draw bird
        bird.draw_bird()

        # Collision
        game_active = bird.check_collision(pipe_list)

        # Draw pipe
        pipe.draw_pipe(pipe_list)

    pygame.display.update()
    world.clock.tick(world.fps_number)