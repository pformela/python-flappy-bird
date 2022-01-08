import pygame as pg
import sys
import random

pg.mixer.init()


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

        self.RESTARTING_BG = pg.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        self.RESTARTING_BG.fill((17, 17, 17))
        self.RESTARTING_BG.convert_alpha()

        self.HIT_BG = pg.Surface((self.settings.WIDTH, self.settings.HEIGHT))
        self.HIT_BG.fill((255, 255, 255))
        self.HIT_BG.convert_alpha()

        # Initialize sounds
        self.HIT_SOUND = pg.mixer.Sound('assets/sounds/hit.mp3')
        self.POINT_SOUND = pg.mixer.Sound('assets/sounds/point.mp3')
        self.WHOOSH_SOUND = pg.mixer.Sound('assets/sounds/whoosh.mp3')

        # Initialize game objects
        self.current_points = 0
        self.highest_score = 0

        self.points = Points(self.settings, 0)
        self.last_digit = Points(self.settings, 0)
        self.point_group = pg.sprite.Group()
        self.point_group.add(self.last_digit)
        self.current_num_of_digits = 1

        self.bird = Bird(self, self.settings, self.points)
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)

        self.grass_first = Grass(0, self, self.settings)
        self.grass_second = Grass(self.settings.WIDTH, self, self.settings)
        self.grass_group = pg.sprite.Group()
        self.grass_group.add(self.grass_first)
        self.grass_group.add(self.grass_second)

        self.sample_pipe = Pipe(-100, random.randrange(-420, -90, 30), self.settings)
        self.first_pipe = Pipe(400, random.randrange(-420, -90, 30), self.settings)
        self.pipe_group = pg.sprite.Group()
        self.pipe_group.add(self.first_pipe)

        self.collision = False

        self.is_restarting = False
        self.restarting_opacity = 3
        self.fading_in = True
        self.i = 0

    def draw_on_screen(self):
        self.WIN.blit(self.BACKGROUND, (0, 0))
        self.pipe_group.draw(self.WIN)
        self.WIN.blit(self.GROUND, (0, self.settings.HEIGHT - self.GROUND.get_height()))
        self.grass_group.draw(self.WIN)
        self.bird_group.draw(self.WIN)
        self.point_group.draw(self.WIN)

        if self.is_restarting is True:
            self.restarting()

        if self.collision is True:
            self.bird_hit_foreground()

        pg.display.flip()
        self.clock.tick(self.settings.FPS)

    def update_screen(self):
        if self.collision is False:
            if self.settings.move_pipes:
                self.pipe_group.update()
            if self.settings.move_grass:
                self.grass_group.update()
        self.update_score()
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
                    self.WHOOSH_SOUND.play()
                if event.key == pg.K_r and self.collision is True and self.settings.can_restart is True:
                    self.is_restarting = True
                    self.fading_in = True

    def handle_pipes(self):
        if self.collision is False:
            for pipe in self.pipe_group:
                index = len(self.pipe_group) - 1

                self.collision = True if pg.sprite.collide_mask(self.bird, pipe) is not None else False

                if self.collision:
                    self.HIT_SOUND.play()
                    self.settings.move_pipes = False
                    self.settings.move_grass = False
                    self.settings.is_bird_moving = False
                    self.settings.is_bird_animating = False
                    break

                if len(self.pipe_group) < 3 and ((self.pipe_group.sprites())[index].rect.left < self.settings.new_x):
                    self.pipe_group.add(Pipe(
                        self.settings.WIDTH,
                        random.randrange(self.sample_pipe.min_y, self.sample_pipe.max_y, 30),
                        self.settings))
                if pipe.rect.right < 0:
                    self.pipe_group.remove(pipe)

    def bird_hit_foreground(self):
        self.WIN.blit(self.HIT_BG, (0, 0))
        self.HIT_BG.set_alpha(self.bird.fade_in_alpha)
        self.bird.fade_in_alpha -= 8 if self.bird.fade_in_alpha > 0 else 0

    def gain_point(self):
        pipe_x = (self.pipe_group.sprites())[0].rect.centerx
        if self.bird.rect.centerx >= pipe_x >= self.bird.rect.centerx - 2 and self.collision is not True:
            self.POINT_SOUND.play()
            self.current_points += 1
            self.current_num_of_digits = len(str(self.current_points))

    def update_score(self):
        for i in range(self.current_num_of_digits):
            if len(self.point_group.sprites()) < self.current_num_of_digits:
                self.point_group.add(Points(self.settings, 1))
            x = int(self.settings.WIDTH//2 - self.current_num_of_digits * self.last_digit.image.get_width() +
                    i * self.last_digit.image.get_width() + self.last_digit.image.get_width())
            self.point_group.sprites()[i].update(x, int(str(self.current_points)[i]))

    def restarting(self):
        self.WIN.blit(self.RESTARTING_BG, (0, 0))
        if self.fading_in is True and self.i <= 255:
            self.RESTARTING_BG.set_alpha(self.i)
            self.i += 15
            if self.i == 255:
                self.fading_in = False
                self.initialize()
        elif self.fading_in is False and self.i > 0:
            self.RESTARTING_BG.set_alpha(self.i)
            self.i -= 15
        elif self.i == 0 and self.fading_in is False:
            self.is_restarting = False

    def initialize(self):

        self.current_points = 0

        self.bird = Bird(self, self.settings, self.points)
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)

        self.collision = False
        self.settings.move_grass = True
        self.settings.can_restart = False
        self.settings.is_bird_animating = True

        self.first_pipe = Pipe(800, random.randrange(-420, -90, 30), self.settings)
        self.pipe_group = pg.sprite.Group()
        self.pipe_group.add(self.first_pipe)


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
        self.objects_speed = 1 * self.SCALE

        self.new_x = self.WIDTH - self.pipe_distance

        self.is_grass_active = True

        self.is_bird_moving = False
        self.is_bird_flying_up = False
        self.is_bird_animating = True

        self.can_restart = False


class Points(pg.sprite.Sprite):

    def __init__(self, settings, current_number):
        super().__init__()
        self.settings = settings

        self.current_number = current_number

        self.zero = pg.image.load("assets/images/numbers/0.png")
        self.zero = pg.transform.scale(
            self.zero, (self.zero.get_width() * self.settings.SCALE, self.zero.get_height() * self.settings.SCALE))
        self.one = pg.image.load("assets/images/numbers/1.png")
        self.one = pg.transform.scale(
            self.one, (self.zero.get_width(), self.zero.get_height()))
        self.two = pg.image.load("assets/images/numbers/2.png")
        self.two = pg.transform.scale(
            self.two, (self.zero.get_width(), self.zero.get_height()))
        self.three = pg.image.load("assets/images/numbers/3.png")
        self.three = pg.transform.scale(
            self.three, (self.zero.get_width(), self.zero.get_height()))
        self.four = pg.image.load("assets/images/numbers/4.png")
        self.four = pg.transform.scale(
            self.four, (self.zero.get_width(), self.zero.get_height()))
        self.five = pg.image.load("assets/images/numbers/5.png")
        self.five = pg.transform.scale(
            self.five, (self.zero.get_width(), self.zero.get_height()))
        self.six = pg.image.load("assets/images/numbers/6.png")
        self.six = pg.transform.scale(
            self.six, (self.zero.get_width(), self.zero.get_height()))
        self.seven = pg.image.load("assets/images/numbers/7.png")
        self.seven = pg.transform.scale(
            self.seven, (self.zero.get_width(), self.zero.get_height()))
        self.eight = pg.image.load("assets/images/numbers/8.png")
        self.eight = pg.transform.scale(
            self.eight, (self.zero.get_width(), self.zero.get_height()))
        self.nine = pg.image.load("assets/images/numbers/9.png")
        self.nine = pg.transform.scale(
            self.nine, (self.zero.get_width(), self.zero.get_height()))

        self.images_list = [self.zero, self.one, self.two, self.three, self.four, self.five, self.six, self.seven,
                            self.eight, self.nine]
        self.image = self.images_list[self.current_number]
        self.rect = self.image.get_rect()
        self.rect.centery = self.settings.HEIGHT//8
        self.rect.centerx = self.settings.WIDTH//2
        # self.digits_list = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def update(self, pos_x, number):
        self.current_number = number
        self.image = self.images_list[self.current_number]
        self.rect.centerx = pos_x


class Bird(pg.sprite.Sprite):

    def __init__(self, game, settings, points):
        super().__init__()
        self.game = game
        self.settings = settings
        self.points = points

        self.init_up_factor = 3 * self.settings.SCALE
        self.init_down_factor = 1
        self.up_factor = 3 * self.settings.SCALE
        self.up_collision_factor = 2 * self.settings.SCALE
        self.down_collision_factor = 1
        self.down_factor = 1

        self.max_down_angle = -35
        self.max_up_angle = 35
        self.current_angle = 0
        self.hit_angle = -90

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

        self.height_of_ground = self.settings.HEIGHT - self.game.GRASS.get_height() - self.game.GROUND.get_height()

        self.pos_x = self.settings.WIDTH//4
        self.pos_y = self.settings.HEIGHT//2
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]

        self.fade_in_alpha = 196

    def update(self):
        if self.settings.is_bird_moving is True:

            self.game.gain_point()

            if self.settings.is_bird_flying_up is False:
                self.rect.y += self.down_factor if (self.rect.bottom < self.height_of_ground) else 0
                self.down_factor += 0.4
                if self.rect.bottom + self.down_factor > self.height_of_ground:
                    self.rect.bottom = self.height_of_ground
            elif self.settings.is_bird_flying_up is True:
                self.down_factor = self.init_down_factor
                self.move()
        elif self.settings.is_bird_moving is False and self.game.collision is True:
            self.hit()

        if self.settings.is_bird_animating is True:
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

    def hit(self):
        if self.up_collision_factor > 0:
            self.rect.y -= self.up_collision_factor
            self.up_collision_factor -= 0.5
        else:
            if self.rect.bottom < self.height_of_ground:
                self.rect.y += self.down_collision_factor
                self.down_collision_factor += 0.4
                if self.rect.bottom + self.down_factor > self.height_of_ground:
                    self.rect.bottom = self.height_of_ground
                    self.settings.can_restart = True

    def jumping(self):
        self.settings.is_bird_moving = True
        self.settings.is_bird_flying_up = True
        self.up_factor = self.init_up_factor

    def move(self):
        if self.up_factor >= 1:
            self.rect.y -= self.up_factor if self.rect.y > 0 else 0
            self.up_factor -= 0.5
            if self.rect.y - self.up_factor <= 0:
                self.rect.y = 0
        else:
            self.up_factor = self.init_up_factor
            self.settings.is_bird_flying_up = False

    def rotate(self, surface, angle):
        rotated_surface = pg.transform.rotozoom(surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        return rotated_surface, rotated_rect


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
