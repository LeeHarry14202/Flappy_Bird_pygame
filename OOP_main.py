import pygame
import sys
import random


pygame.init()

# Set screen
SCREEN_WIDTH = 216
SCREEN_HEIGHT = 384
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class World(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gravity = 0.25
        # Set fps
        self.clock = pygame.time.Clock()
        self.fps_number = 90
        # Game status
        self.game_active = True

    def draw_(self, image, x, y):
        screen.blit(image, (x, y))


class BACKGROUND(World):
    def __init__(self):
        super().__init__()
        # Set background location
        self.x_background = 0
        self.y_background = 0
        self.image = IMAGE.background_img


class FLOOR(World):
    def __init__(self):
        super().__init__()
        # Set floor location
        self.x_floor = 0
        self.y_floor = SCREEN_HEIGHT * 0.75
        self.image = IMAGE.floor_img

    def draw_(self, image, x, y):
        screen.blit(image, (x, y))
        x += SCREEN_WIDTH
        screen.blit(image, (x, y))


class BIRD(World):
    def __init__(self):
        super().__init__()
        # Set bird location
        self.x_bird = SCREEN_WIDTH / 3
        self.y_bird = SCREEN_HEIGHT / 2
        self.image = IMAGE.bird_mid
        self.rect = self.image.get_rect(center=(self.x_bird, self.y_bird))
        self.bird_movement = 0
        # List bird
        self.bird_list = [IMAGE.bird_down, IMAGE.bird_mid, IMAGE.bird_up]
        self.bird_index = 0
        self.bird_in_list = self.bird_list[self.bird_index]

    def draw_bird(self, image, rect):
        self.jump()
        screen.blit(image, rect)

    def jump(self):
        self.bird_movement += world.gravity
        self.rect.centery += self.bird_movement
        return self.rect

    def rotate_bird(self, bird_):
        new_bird = pygame.transform.rotozoom(bird_, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_list[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(self.x_bird, self.rect.centery))
        return new_bird, new_bird_rect

    def check_collision(self, pipes):
        for pipe_ in pipes:
            # If bird hit the pipe return False
            if self.rect.colliderect(pipe_):
                SFX.hit_sound.play()
                return False
        # If bird go out of screen return False         
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            SFX.hit_sound.play()
            return False
        return True


class PIPE(World):
    def __init__(self):
        super().__init__()
        self.pipe_height = [SCREEN_HEIGHT/2, SCREEN_HEIGHT/1.5, SCREEN_HEIGHT/3]
        self.image = IMAGE.pipe_img
        self.pipe_list = []

    def create_pipe(self):
        random_pipe_y_pos = random.choice(self.pipe_height)
        x_pipe = SCREEN_WIDTH
        y_pipe = random_pipe_y_pos
        bottom_pipe = IMAGE.pipe_img.get_rect(midtop=(x_pipe, y_pipe))
        top_pipe = IMAGE.pipe_img.get_rect(midtop=(x_pipe, y_pipe - SCREEN_HEIGHT))
        return bottom_pipe, top_pipe

    def move_pipe(self, pipes):
        for pipe_ in pipes:
            pipe_.centerx -= 2
        return pipes

    def draw_pipe(self, pipes):
        pipes = self.move_pipe(pipes)
        for pipe_ in pipes:
            if pipe_.bottom >= SCREEN_HEIGHT * (9 / 10):
                screen.blit(IMAGE.pipe_img, pipe_)
            else:
                # Only flip y_axis
                flip_pipe = pygame.transform.flip(IMAGE.pipe_img, False, True)
                screen.blit(flip_pipe, pipe_)


class SCORE(World):
    def __init__(self):
        super().__init__()
        self.current_score = 0
        self.high_score = 0
        self.score_sound_countdown = 100
        # Set game font
        font_size = 20
        self.font_color = (255, 255, 255)
        self.game_font = pygame.font.Font('04B_19.TTF', font_size)
        # Set score location
        self.x_score = SCREEN_WIDTH / 2
        self.y_score = SCREEN_HEIGHT / 6
        # Set high score location
        self.x_high_score = SCREEN_WIDTH / 2
        self.y_high_score = SCREEN_HEIGHT / 10

    def score_display(self, game_state):

        if game_state == 'main game':
            score_surface = self.game_font.render(str(int(self.current_score)), True, self.font_color)
            score_rect = score_surface.get_rect(center=(self.x_score, self.y_score))
            screen.blit(score_surface, score_rect)
        if game_state == 'game over':
            # Display score
            score_surface = self.game_font.render(f"High Score: {str(int(self.high_score))}", True, self.font_color)
            score_rect = score_surface.get_rect(center=(self.x_high_score, self.y_high_score))
            screen.blit(score_surface, score_rect)
            # Display high score
            high_score_surface = self.game_font.render(str(int(self.current_score)), True, self.font_color)
            high_score_rect = high_score_surface.get_rect(center=(self.x_score, self.y_score))
            screen.blit(high_score_surface, high_score_rect)

    def update_score(self, score_, high_score):
        if score_ > high_score:
            high_score = score_
        return high_score


# Sound class and Music loading
def load_sound(sound_location):
    sound = pygame.mixer.Sound(sound_location)
    return sound


class SFX:
    # Create sound
    flap_sound = load_sound('./sound/sfx_wing.wav')
    hit_sound = load_sound('./sound/sfx_hit.wav')
    point_sound = load_sound('./sound/sfx_point.wav')


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    return image


# Image class and image loading
class IMAGE:
    # Load image
    background_img = load_image('./assests/background-night.png')
    floor_img = load_image('./assests/floor.png')
    bird_down = load_image('./assests/yellowbird-downflap.png')
    bird_up = load_image('./assests/yellowbird-upflap.png')
    bird_mid = load_image('./assests/yellowbird-midflap.png')
    pipe_img = load_image('./assests/pipe-green.png')
    game_ready_surface = load_image('./assests/message.png')


# Set timer for pipe
spawn_pipe = pygame.USEREVENT
spawn_pipe_time = 1200
pygame.time.set_timer(spawn_pipe, spawn_pipe_time)

# Set timer for bird wing
bird_flap = pygame.USEREVENT + 1
bird_flap_timer = 200
pygame.time.set_timer(bird_flap, bird_flap_timer)


# Create ready background
game_ready_rect = IMAGE.game_ready_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Object init
world = World()
background = BACKGROUND()
bird = BIRD()
pipe = PIPE()
floor = FLOOR()
score = SCORE()


def main():
    game_active = world.game_active
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.bird_movement = -5.5
                    SFX.flap_sound.play()
                    # Play again
                if event.key == pygame.K_SPACE and game_active is False:
                    game_active = True
                    # Reset pipe list
                    pipe.pipe_list.clear()
                    # Reset bird location at center of y
                    bird.rect.center = (bird.x_bird, bird.y_bird)
                    bird.bird_movement = 0
            if event.type == spawn_pipe:
                pipe.pipe_list.extend(pipe.create_pipe())
            if event.type == bird_flap:
                if bird.bird_index < 2:
                    bird.bird_index += 1
                else:
                    bird.bird_index = 0
                bird_one, bird.rect = bird.bird_animation()

        # Draw background
        world.draw_(background.image, background.x_background, background.y_background)

        # Draw floor
        floor.x_floor -= 1
        floor.draw_(floor.image, floor.x_floor, floor.y_floor)
        if floor.x_floor <= -SCREEN_WIDTH:
            floor.x_floor = 0

        if game_active:
            # Create a function to rotate bird
            rotated_bird = bird.rotate_bird(bird.bird_in_list)

            # Draw bird
            bird.draw_bird(rotated_bird, bird.rect)

            # Collision
            game_active = bird.check_collision(pipe.pipe_list)

            # Draw pipe
            pipe.draw_pipe(pipe.pipe_list)

            # Score
            score.current_score += 0.01
            score.score_display('main game')
            score.score_sound_countdown -= 1
            if score.score_sound_countdown == 0:
                SFX.point_sound.play()
                score.score_sound_countdown = 100
        else:
            screen.blit(IMAGE.game_ready_surface, game_ready_rect)
            # Update high score
            score.high_score = score.update_score(score.current_score, score.high_score)
            score.score_display('game over')
            # Reset current score to 0
            score.current_score = 0

        pygame.display.update()
        world.clock.tick(world.fps_number)


if __name__ == "__main__":
    main()
    