import pygame as pg
import sys
import random


class Game:

    def __init__(self, settings):

        self.settings = settings

        # Initialize game
        self.clock = pg.time.Clock()
        pg.init()

        # Initialize window
        self.WIN = pg.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pg.display.set_caption("Flappy Bird")

        # Initialize pictures
        self.BACKGROUND = pg.transform.scale(pg.image.load('assets/images/background.png'),
                                             (self.settings.WIDTH, self.settings.HEIGHT))

        self.GROUND = pg.image.load('assets/images/ground.png')
        self.GROUND = pg.transform.scale(
            self.GROUND,
            (self.GROUND.get_width() * self.settings.SCALE, self.GROUND.get_height() * self.settings.SCALE))

        self.GRASS = pg.image.load('assets/images/grass.png')
        self.GRASS = pg.transform.scale(self.GRASS,
                                        (self.GRASS.get_width() * self.settings.SCALE,
                                         self.GRASS.get_height() * self.settings.SCALE))

        self.BIRD = pg.image.load('assets/images/bird1.png')
        self.BIRD = pg.transform.scale(self.BIRD,
                                       (self.BIRD.get_width() * self.settings.SCALE,
                                        self.BIRD.get_height() * self.settings.SCALE))

        # Initialize game objects
        self.bird = Bird(self, self.settings)
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)

        self.grass_first = Grass(0, self, self.settings)
        self.grass_second = Grass(self.settings.WIDTH, self, self.settings)
        self.grass_group = pg.sprite.Group()
        self.grass_group.add(self.grass_first)
        self.grass_group.add(self.grass_second)

        self.sample_pipe = Pipe(-100, random.randrange(-420, -90, 30), self.settings)
        self.first_pipe = Pipe(800, random.randrange(-420, -90, 30), self.settings)
        self.pipe_group = pg.sprite.Group()
        self.pipe_group.add(self.first_pipe)

        self.collision = False

    def draw_on_screen(self):
        self.WIN.blit(self.BACKGROUND, (0, 0))
        self.pipe_group.draw(self.WIN)
        self.WIN.blit(self.GROUND, (0, self.settings.HEIGHT - self.GROUND.get_height()))
        self.grass_group.draw(self.WIN)
        self.bird_group.draw(self.WIN)

        pg.display.flip()
        self.clock.tick(self.settings.FPS)

    def update_screen(self):
        if not self.collision:
            if self.settings.move_pipes:
                self.pipe_group.update()
            if self.settings.move_grass:
                self.grass_group.update()
            if self.settings.is_bird_animating:
                self.bird_group.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not self.collision:
                    self.settings.move_pipes = True
                    self.bird.jumping()

    def handle_pipes(self):
        for pipe in self.pipe_group:
            index = len(self.pipe_group) - 1

            self.collision = True if pg.sprite.collide_mask(self.bird, pipe) is not None else False

            if self.collision:
                self.settings.move_pipes = False
                self.settings.move_grass = False
                self.settings.is_bird_moving = False
                self.settings.is_bird_animating = False
                break

            if len(self.pipe_group) < 3 and \
                    ((self.pipe_group.sprites())[index].rect.left < self.settings.WIDTH - self.settings.pipe_distance):
                self.pipe_group.add(Pipe(self.settings.WIDTH,
                                    random.randrange(self.sample_pipe.min_y, self.sample_pipe.max_y, 30),
                                         self.settings))
            if pipe.rect.right < 0:
                self.pipe_group.remove(pipe)


class Settings:

    def __init__(self):
        self.SCALE = 3
        self.WIDTH = self.SCALE * 144
        self.HEIGHT = self.SCALE * 256

        self.FPS = 60

        self.move_pipes = False
        self.move_grass = True
        self.game_running = True

        self.pipe_min_y = -140 * self.SCALE
        self.pipe_max_y = -30 * self.SCALE
        self.pipe_distance = 83 * self.SCALE
        self.objects_speed = 3

        self.is_grass_active = True

        self.is_bird_moving = False
        self.is_bird_flying_up = False
        self.is_bird_animating = True


class Bird(pg.sprite.Sprite):

    def __init__(self, game, settings):
        super().__init__()
        self.game = game
        self.settings = settings

        self.change_y = 1
        self.init_up_factor = 10
        self.init_down_factor = 1
        self.up_factor = 10
        self.down_factor = 1
        self.speed = 0.5

        self.sprites = []
        self.bird1 = pg.image.load('assets/images/bird1.png')
        self.bird2 = pg.image.load('assets/images/bird2.png')
        self.bird3 = pg.image.load('assets/images/bird3.png')
        self.bird1 = pg.transform.scale(self.bird1, (self.game.BIRD.get_width(), self.game.BIRD.get_height()))
        self.bird2 = pg.transform.scale(self.bird2, (self.game.BIRD.get_width(), self.game.BIRD.get_height()))
        self.bird3 = pg.transform.scale(self.bird3, (self.game.BIRD.get_width(), self.game.BIRD.get_height()))
        self.sprites.append(self.bird1)
        self.sprites.append(self.bird2)
        self.sprites.append(self.bird3)
        self.sprites.append(self.bird2)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.mask = pg.mask.from_surface(self.image)

        self.pos_x = self.settings.WIDTH//4
        self.pos_y = self.settings.HEIGHT//2
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]

    def update(self):
        if self.settings.is_bird_moving:
            if not self.settings.is_bird_flying_up:
                self.rect.y += int(self.change_y * self.down_factor) \
                    if (self.rect.bottom < self.settings.HEIGHT - self.game.GRASS.get_height() -
                        self.game.GROUND.get_height()) else 0
                self.down_factor += (self.speed - 0.1) if self.down_factor <= 20 else 0
            else:
                self.down_factor = self.init_down_factor
                self.move()

        if self.settings.is_bird_animating:
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

    def jumping(self):
        self.settings.is_bird_moving = True
        self.settings.is_bird_flying_up = True
        self.up_factor = self.init_up_factor

    def move(self):
        if self.up_factor >= 1:
            self.rect.y -= int(self.change_y * self.up_factor) if self.rect.y > 0 else 0
            self.up_factor -= (self.speed + 0.1)
        else:
            self.up_factor = self.init_up_factor
            self.settings.is_bird_flying_up = False


class Pipe(pg.sprite.Sprite):

    def __init__(self, pos_x, pos_y, settings):
        super().__init__()
        self.settings = settings

        self.image = pg.image.load('assets/images/pipes.png')
        self.image = pg.transform.scale(self.image,
                                        (self.image.get_width() * self.settings.SCALE,
                                         self.image.get_height() * self.settings.SCALE))

        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.rect.x = pos_x
        self.rect.y = pos_y

        self.min_y = -140 * self.settings.SCALE
        self.max_y = -30 * self.settings.SCALE
        self.distance = 250

    def update(self):
        self.rect.x -= self.settings.objects_speed


class Grass(pg.sprite.Sprite):

    def __init__(self, pos_x, game, settings):
        super().__init__()
        self.settings = settings
        self.game = game
        self.image = self.game.GRASS

        self.rect = self.image.get_rect()
        self.rect.y = self.settings.HEIGHT - self.game.GROUND.get_height() - self.game.GRASS.get_height()
        self.rect.x = pos_x
        self.pos_x = pos_x

    def update(self):
        if self.settings.is_grass_active:
            if self.rect.right <= self.pos_x:
                self.rect.x = self.pos_x

            self.rect.x -= self.settings.objects_speed


def main():

    settings = Settings()
    game = Game(settings)

    while settings.game_running:
        game.draw_on_screen()
        game.update_screen()
        game.handle_pipes()
        game.handle_events()


if __name__ == "__main__":
    main()
