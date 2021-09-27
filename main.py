import pygame
import sys
import random


def draw_floor(x_floor):
    screen.blit(floor, (x_floor, y_floor))
    x_floor = x_floor + x_screen
    screen.blit(floor, (x_floor, y_floor))


def create_bird():
    bird_rect = bird.get_rect(center=(x_bird, y_bird))
    return bird_rect


def rotate_bird(bird_one):
    new_bird = pygame.transform.rotozoom(bird_one, -bird_movement*3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(x_bird, bird_rect.centery))
    return new_bird, new_bird_rect


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    x_pipe = x_screen 
    y_pipe = random_pipe_pos
    bottom_pipe = pipe_surface.get_rect(midtop=(x_pipe, y_pipe))
    top_pipe = pipe_surface.get_rect(midtop=(x_pipe, y_pipe - y_screen))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes


def draw_pipe(pipes): 
    for pipe in pipes:
        if pipe.bottom >= y_screen * (9/10):
            screen.blit(pipe_surface, pipe)
        else:
            # Only flip y_axis
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= Oy or bird_rect.bottom >= y_screen:
        hit_sound.play()
        return False
    return True


def score_display(game_state):
    font_color = (255, 255, 255)
    x_score = x_screen / 2
    y_score = y_screen / 6
    x_high_score = x_screen / 2
    y_high_score = y_screen / 10
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, font_color)
        score_rect = score_surface.get_rect(center=(x_score, y_score))
        screen.blit(score_surface, score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f"High Score: {str(int(high_score))}", True, font_color)
        score_rect = score_surface.get_rect(center=(x_high_score, y_high_score))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(str(int(score)), True, font_color)
        high_score_rect = high_score_surface.get_rect(center=(x_score, y_score))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
pygame.init()


# Set screen
x_screen = 216
y_screen = 384
screen = pygame.display.set_mode((x_screen, y_screen))

game_active = True

# Set fps
clock = pygame.time.Clock()
fps_number = 90


# O(0,0)
Ox = 0
Oy = 0

# Set game font
font_size = 20
game_font = pygame.font.Font('04B_19.TTF', font_size)

# Set score and high score
score = 0
high_score = 0

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
x_bird = x_screen / 3
y_bird = y_screen / 2
# Convert have pygame load img faster, convert_alpha remove black box
bird_down = pygame.image.load('./assests/yellowbird-downflap.png').convert_alpha()
bird_up = pygame.image.load('./assests/yellowbird-upflap.png').convert_alpha()
bird_mid = pygame.image.load('./assests/yellowbird-midflap.png').convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = create_bird()

# Set timer for bird wing
bird_flap = pygame.USEREVENT + 1
bird_flap_timer = 200
pygame.time.set_timer(bird_flap, bird_flap_timer)

# Create gravity
gravity = 0.25
# Bird not move yet
bird_movement = 0


# Create pipe
pipe_surface = pygame.image.load('./assests/pipe-green.png').convert()
pipe_list = []


# Create timer for pipe
spawnpipe = pygame.USEREVENT
# New pipe will appear in every 1200 ms
spawnpipe_time = 1200
pygame.time.set_timer(spawnpipe, spawnpipe_time)
pipe_height = [y_screen/2, y_screen/1.5, y_screen/3]

# Create finished background
game_over_surface = (pygame.image.load('./assests/gameover.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(x_screen/2, y_screen/2))

# Create ready background
game_ready_surface = pygame.image.load('./assests/message.png').convert_alpha()
game_ready_rect = game_ready_surface.get_rect(center=(x_screen/2, y_screen/2))

# Create sound
flap_sound = pygame.mixer.Sound('./sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('./sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('./sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -5.5
                flap_sound.play()
            # Play again
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                # reset pipe list
                pipe_list.clear()
                bird_rect.center = (x_bird, y_bird)
                bird_movement = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # Draw background
    screen.blit(background, (x_background, y_background))

    # Draw floor
    x_floor -= 1
    draw_floor(x_floor)
    if x_floor <= -x_screen:
        x_floor = Ox

    if game_active:
        # Draw bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        # Create a function to rotate bird
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)

        # Collision
        game_active = check_collision(pipe_list)

        # Draw pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            point_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_ready_surface, game_ready_rect)
        # Reset score
        high_score = update_score(score, high_score)
        score_display('game over')
        score = 0

    pygame.display.update()
    clock.tick(fps_number)