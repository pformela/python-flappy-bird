import pygame
import sys
import random

SCALE = 3
WIDTH = SCALE * 144
HEIGHT = SCALE * 256

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BACKGROUND = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (WIDTH, HEIGHT))
GROUND = pygame.image.load('assets/images/ground.png')
GROUND = pygame.transform.scale(GROUND, (GROUND.get_width() * SCALE, GROUND.get_height() * SCALE))
GRASS = pygame.image.load('assets/images/grass.png')
GRASS = pygame.transform.scale(GRASS, (GRASS.get_width() * SCALE, GRASS.get_height() * SCALE))
BIRD = pygame.image.load('assets/images/bird1.png')
BIRD = pygame.transform.scale(BIRD, (BIRD.get_width() * SCALE, BIRD.get_height() * SCALE))

clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):

    def __init__(self, pos_y):
        super().__init__()
        self.is_animating = True
        self.start_jumping = False
        self.is_jumping = False
        self.change_y = 1
        self.init_up_factor = 10
        self.init_down_factor = 1
        self.up_factor = 10
        self.down_factor = 1
        self.speed = 0.5

        self.sprites = []
        self.bird1 = pygame.image.load('assets/images/bird1.png')
        self.bird2 = pygame.image.load('assets/images/bird2.png')
        self.bird3 = pygame.image.load('assets/images/bird3.png')
        self.bird1 = pygame.transform.scale(self.bird1, (BIRD.get_width(), BIRD.get_height()))
        self.bird2 = pygame.transform.scale(self.bird2, (BIRD.get_width(), BIRD.get_height()))
        self.bird3 = pygame.transform.scale(self.bird3, (BIRD.get_width(), BIRD.get_height()))
        self.sprites.append(self.bird1)
        self.sprites.append(self.bird2)
        self.sprites.append(self.bird3)
        self.sprites.append(self.bird2)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.pos_x = WIDTH//4
        self.pos_y = pos_y
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]

        self.rotated_rect = self.rect
        self.rotated_surface = self.image

    def update(self):
        if self.start_jumping:
            if not self.is_jumping:
                self.rect.y += int(self.change_y * self.down_factor) \
                    if (self.rect.bottom < HEIGHT - GRASS.get_height() - GROUND.get_height()) else 0
                self.down_factor += (self.speed - 0.1) if self.down_factor <= 20 else 0
            else:
                self.down_factor = self.init_down_factor
                self.move()

        self.current_sprite += 0.2

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

    def jumping(self):
        self.start_jumping = True
        self.is_jumping = True
        self.up_factor = self.init_up_factor

    def move(self):
        if self.up_factor >= 1:
            self.rect.y -= int(self.change_y * self.up_factor) if self.rect.y > 0 else 0
            self.up_factor -= (self.speed + 0.1)
        else:
            self.up_factor = self.init_up_factor
            self.is_jumping = False

    def rotate(self, surface, angle):
        self.rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
        self.rotated_rect = self.rotated_surface.get_rect()


class Pipe(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('assets/images/pipes.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_width() * SCALE, self.image.get_height() * SCALE))

        self.rect = self.image.get_rect()

        self.rect.x = pos_x
        self.rect.y = pos_y

        self.min_y = -140 * SCALE
        self.max_y = -30 * SCALE
        self.distance = 250
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed


class Grass(pygame.sprite.Sprite):

    def __init__(self, pos_x):
        super().__init__()
        self.image = GRASS

        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - GROUND.get_height() - GRASS.get_height()
        self.rect.x = pos_x

        self.pos_x = pos_x

        self.speed = 3

    def update(self):
        if self.rect.right <= self.pos_x:
            self.rect.x = self.pos_x

        self.rect.x -= self.speed


def main():

    pygame.init()

    bird = Bird(HEIGHT//2)
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)

    grass = Grass(0)
    grass2 = Grass(WIDTH)
    grass_group = pygame.sprite.Group()
    grass_group.add(grass)
    grass_group.add(grass2)

    sample_pipe = Pipe(-100, random.randrange(-420, -90, 30))
    first_pipe = Pipe(800, random.randrange(-420, -90, 30))
    pipe_group = pygame.sprite.Group()
    pipe_group.add(first_pipe)
    move_pipes = False

    running = True

    while running:

        WIN.blit(BACKGROUND, (0, 0))
        pipe_group.draw(WIN)
        WIN.blit(GROUND, (0, HEIGHT - GROUND.get_height()))
        grass_group.draw(WIN)
        grass_group.update()
        bird_group.draw(WIN)
        bird_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    move_pipes = True
                    bird.jumping()

        for pipe in pipe_group:
            index = len(pipe_group) - 1
            if len(pipe_group) < 3 and ((pipe_group.sprites())[index].rect.left < WIDTH - 240):
                pipe_group.add(Pipe(WIDTH, random.randrange(sample_pipe.min_y, sample_pipe.max_y, 30)))
            if pipe.rect.right < 0:
                pipe_group.remove(pipe)

        if move_pipes:
            pipe_group.update()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
