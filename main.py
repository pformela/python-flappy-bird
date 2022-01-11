import pygame as pg
import sys
import random as r
from settings import Settings
from bird import Bird
from ground import Ground
from pipe import Pipe
from points import Points


pg.mixer.pre_init(frequency=44100)
pg.init()
pg.mixer.init(frequency=44100)


class Game:

    def __init__(self, settings):

        self.s = settings

        # Initialize game
        self.clock = pg.time.Clock()
        pg.init()

        # Initialize window
        self.WIN = pg.display.set_mode((self.s.WIDTH, self.s.HEIGHT))
        pg.display.set_caption("Flappy Bird")

        # Initialize graphics
        self.BACKGROUND = pg.transform.scale(pg.image.load('assets/images/background.png'),
                                             (self.s.WIDTH, self.s.HEIGHT))
        self.GROUND = pg.image.load('assets/images/ground.png')
        self.GROUND = pg.transform.scale(self.GROUND, (self.GROUND.get_width() * self.s.SCALE,
                                                       self.GROUND.get_height() * self.s.SCALE))
        self.BIRD = pg.image.load('assets/images/bird1.png')
        self.BIRD = pg.transform.scale(self.BIRD,
                                       (self.BIRD.get_width() * self.s.SCALE,
                                        self.BIRD.get_height() * self.s.SCALE))
        self.RESTARTING_BG = pg.Surface((self.s.WIDTH, self.s.HEIGHT))
        self.RESTARTING_BG.fill((17, 17, 17))
        self.RESTARTING_BG.convert_alpha()
        self.HIT_BG = pg.Surface((self.s.WIDTH, self.s.HEIGHT))
        self.HIT_BG.fill((255, 255, 255))
        self.HIT_BG.convert_alpha()

        self.GET_READY = pg.image.load('assets/images/getready.png')
        self.GET_READY = pg.transform.scale(self.GET_READY, (self.GET_READY.get_width() * self.s.SCALE,
                                                             self.GET_READY.get_height() * self.s.SCALE))
        self.GET_READY.convert_alpha()
        self.get_ready_alpha = 255

        self.SPACE = pg.image.load('assets/images/press_space.png')
        self.SPACE = pg.transform.scale(self.SPACE, (self.SPACE.get_width() * self.s.SCALE,
                                                     self.SPACE.get_height() * self.s.SCALE))
        self.SPACE.convert_alpha()

        # Initialize scoreboard
        self.SCOREBOARD = pg.image.load('assets/images/scoreboard.png')
        self.SCOREBOARD = pg.transform.scale(self.SCOREBOARD, (self.SCOREBOARD.get_width() * self.s.SCALE,
                                                               self.SCOREBOARD.get_height() * self.s.SCALE))
        self.SCOREBOARD.convert_alpha()
        self.scoreboard_y = self.s.HEIGHT
        self.scoreboard_x = self.s.WIDTH//2 - self.SCOREBOARD.get_width()//2
        self.scoreboard_y_change = 55
        self.scoreboard_alpha = 255

        # Initialize sounds
        self.HIT_SOUND = pg.mixer.Sound('assets/sounds/hit.mp3')
        self.POINT_SOUND = pg.mixer.Sound('assets/sounds/point.mp3')
        self.WHOOSH_SOUND = pg.mixer.Sound('assets/sounds/whoosh.mp3')

        # Initialize game objects
        self.current_points = 0
        self.high_score = 0

        self.small_point = Points(self.s, 0, 0, 1, 0, 0)
        self.point = Points(self.s, 0, 0)

        self.last_digit = Points(self.s, 0, 0)
        self.point_group = pg.sprite.Group()
        self.point_group.add(self.last_digit)

        self.len_score = len(str(self.current_points))
        self.points_alpha = 0
        self.current_score_alpha = 0
        self.are_points_updated = False

        self.high_score_group = pg.sprite.Group()
        self.current_score_group = pg.sprite.Group()

        self.bird = Bird(self, self.s)
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)

        self.ground_group = pg.sprite.Group()
        self.ground_group.add(Ground(self, self.s))

        self.sample_pipe = Pipe(-100, r.randrange(-420, -90, 30), self.s)
        self.first_pipe = Pipe(self.s.pipe_distance * self.s.SCALE, r.randrange(-420, -90, 30), self.s)
        self.pipe_group = pg.sprite.Group()
        self.pipe_group.add(self.first_pipe)

        self.collision = False
        self.start_game = False
        self.is_restarting = False
        self.wait_for_scoreboard = 60
        self.restarting_opacity = 3
        self.fading_in = True
        self.i = 0

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                self.keydown_events(event)

    def keydown_events(self, event):
        if event.key == pg.K_SPACE and not self.collision:
            self.start_game = True
            self.s.move_pipes = True
            self.bird.initialize_ascend()
            self.WHOOSH_SOUND.play()
        if event.key == pg.K_r and self.collision is True and self.s.can_restart is True:
            self.is_restarting = True
            self.fading_in = True

    def update_screen(self):
        if self.collision is False:
            if self.s.move_pipes:
                self.handle_pipes()
                self.pipe_group.update()
            if self.s.move_ground:
                self.ground_group.update()

        self.update_score()
        self.bird_group.update()

    def draw_on_screen(self):
        self.WIN.blit(self.BACKGROUND, (0, 0))
        self.pipe_group.draw(self.WIN)
        self.ground_group.draw(self.WIN)
        self.bird_group.draw(self.WIN)
        self.point_group.draw(self.WIN)

        if self.collision is True:
            self.flash()
            self.show_scoreboard()
            self.current_score_group.draw(self.WIN)
            self.high_score_group.draw(self.WIN)

        if self.is_restarting is True:
            self.restarting()

        self.show_get_ready()

        pg.display.flip()
        self.clock.tick(self.s.FPS)

    def handle_pipes(self):
        for pipe in self.pipe_group:
            index = len(self.pipe_group) - 1

            self.collision = True if pg.sprite.collide_mask(self.bird, pipe) is not None else False
            if self.collision:
                self.stop_game()
                break

            if len(self.pipe_group) < 3 and ((self.pipe_group.sprites())[index].rect.left < self.s.new_x):
                self.add_pipe(self.s.WIDTH, r.randrange(self.s.min_pipe_y, self.s.max_pipe_y, 30), self.s)
            if pipe.rect.right < 0:
                self.pipe_group.remove(pipe)

    def add_pipe(self, x, y, settings):
        self.pipe_group.add(Pipe(x, y, settings))

    def flash(self):
        self.WIN.blit(self.HIT_BG, (0, 0))
        self.HIT_BG.set_alpha(self.bird.flash_alpha)
        self.bird.flash_alpha -= 8 if self.bird.flash_alpha > 0 else 0

    def gain_point(self):
        pipe_x = (self.pipe_group.sprites())[0].rect.centerx
        if self.bird.rect.centerx >= pipe_x >= self.bird.rect.centerx - 2 and self.collision is not True:
            self.POINT_SOUND.play()
            self.current_points += 1
            self.len_score = len(str(self.current_points))

    def update_score(self):
        for i in range(self.len_score):
            curr_sprite = self.point_group.sprites()[i]
            self.add_digit()

            x = self.score_digit_posx(i)
            if self.start_game is True or self.collision is True:
                curr_sprite.update(int(str(self.current_points)[i]), self.points_alpha, x)
            else:
                curr_sprite.update(int(str(self.current_points)[i]), 0, x)

        self.fade_score()

    def fade_score(self):
        if self.collision is True and self.bird.rect.bottom + 10 >= self.bird.ground_height:
            self.points_alpha -= 15 if self.points_alpha > 0 else 0
        elif self.start_game is True and self.collision is False:
            self.points_alpha += 15 if self.points_alpha < 255 else 0

    def add_digit(self):
        if len(self.point_group.sprites()) < self.len_score:
            self.point_group.add(Points(self.s, 1, 255))

    def score_digit_posx(self, i):
        if self.len_score % 2 == 0:
            x = (int(self.s.WIDTH // 2 - (self.len_score / 2) * self.point.w + self.point.w * i + self.point.w // 2))
        else:
            x = (int(self.s.WIDTH // 2 - self.len_score // 2 * self.point.w + i * self.point.w))
        return x

    def show_scoreboard(self):
        if self.wait_for_scoreboard > 0:
            self.wait_for_scoreboard -= 1
        else:
            self.WIN.blit(self.SCOREBOARD, (self.scoreboard_x, self.scoreboard_y))

            if self.are_points_updated is False:
                self.update_final_score()

            if self.scoreboard_y > self.s.HEIGHT * 0.3:
                self.move_scoreboard_up()
            else:
                self.fade_in_final_score()

    def update_final_score(self):
        if self.high_score <= self.current_points:
            self.high_score = self.current_points
            self.high_score_group = pg.sprite.Group()

        for i in range(self.len_score):
            self.current_score_group.add(
                Points(self.s, int(str(self.current_points)[i]), 0, 1,
                       114 * self.s.SCALE - (self.len_score - i - 1) * self.small_point.w + 2, 96 * self.s.SCALE))
            if self.high_score <= self.current_points:
                self.high_score_group.add(
                    Points(self.s, int(str(self.current_points)[i]), 0, 1,
                           114 * self.s.SCALE - (self.len_score - i - 1) * self.small_point.w + 2, 117 * self.s.SCALE))

        self.are_points_updated = True

    def move_scoreboard_up(self):
        self.scoreboard_y -= self.scoreboard_y_change
        self.scoreboard_y_change -= 2.5

    def fade_in_final_score(self):
        for i in range(len(self.current_score_group.sprites())):
            self.current_score_group.sprites()[i].image.set_alpha(self.current_score_alpha)
        for i in range(len(self.high_score_group.sprites())):
            self.high_score_group.sprites()[i].image.set_alpha(self.current_score_alpha)
        self.current_score_alpha += 5 if self.current_score_alpha < 255 else 0

    def show_get_ready(self):
        self.WIN.blit(self.GET_READY, (self.s.WIDTH//2 - self.GET_READY.get_width()//2, self.s.HEIGHT//6))
        self.WIN.blit(self.SPACE, (self.s.WIDTH//2 - self.SPACE.get_width()//2, self.s.HEIGHT//2))
        if self.start_game is True and self.get_ready_alpha >= 0:
            self.SPACE.set_alpha(self.get_ready_alpha)
            self.GET_READY.set_alpha(self.get_ready_alpha)
            self.get_ready_alpha -= 15

    def restarting(self):
        self.WIN.blit(self.RESTARTING_BG, (0, 0))
        if self.fading_in is True and self.i <= 255:
            for i in range(len(self.current_score_group.sprites())):
                self.current_score_group.sprites()[i].image.set_alpha(255-self.i)
            for i in range(len(self.high_score_group.sprites())):
                self.high_score_group.sprites()[i].image.set_alpha(255-self.i)
            self.RESTARTING_BG.set_alpha(self.i)
            self.SCOREBOARD.set_alpha(255-self.i)
            self.i += 15
            if self.i == 255:
                self.SCOREBOARD.set_alpha(255)
                self.fading_in = False
                self.initialize()
        elif self.fading_in is False and self.i > 0:
            self.RESTARTING_BG.set_alpha(self.i)
            self.GET_READY.set_alpha(255 - self.i)
            self.SPACE.set_alpha(255 - self.i)
            self.i -= 15
        elif self.i == 0 and self.fading_in is False:
            for i in range(len(self.high_score_group.sprites())):
                self.high_score_group.sprites()[i].image.set_alpha(0)
            self.is_restarting = False

    def stop_game(self):
        self.HIT_SOUND.play()
        self.high_score = self.current_points if self.current_points > self.high_score else self.high_score
        self.s.move_pipes = False
        self.s.move_ground = False
        self.s.is_bird_moving = False
        self.s.is_bird_animating = False

    def initialize(self):
        self.current_points = 0
        self.len_score = 1
        self.current_score_group = pg.sprite.Group()
        self.get_ready_alpha = 255
        self.start_game = False
        self.points_alpha = 0
        self.current_score_alpha = 0
        self.scoreboard_y = self.s.HEIGHT
        self.scoreboard_y_change = 55
        self.wait_for_scoreboard = 60
        self.are_points_updated = False

        self.bird = Bird(self, self.s)
        self.bird_group = pg.sprite.Group()
        self.bird_group.add(self.bird)

        self.collision = False
        self.s.move_ground = True
        self.s.can_restart = False
        self.s.is_bird_animating = True

        self.first_pipe = Pipe(self.s.pipe_distance * self.s.SCALE, r.randrange(-420, -90, 30), self.s)
        self.pipe_group = pg.sprite.Group()
        self.pipe_group.add(self.first_pipe)


def main():

    settings = Settings()
    game = Game(settings)

    while settings.game_running:
        game.update_screen()
        game.draw_on_screen()
        game.handle_events()


if __name__ == "__main__":
    main()
