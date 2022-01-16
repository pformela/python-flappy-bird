import pygame as pg


class Bird(pg.sprite.Sprite):

    def __init__(self, game, settings):
        super().__init__()
        self.game = game
        self.s = settings

        # initializing ascending and descending y position values
        self.init_up_factor = 3 * self.s.SCALE
        self.init_down_factor = 1
        self.up_factor = 3 * self.s.SCALE
        self.up_collision_factor = 2 * self.s.SCALE
        self.down_collision_factor = 1
        self.down_factor = 1

        # load images to animate bird's wings
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

        self.ground_height = self.s.HEIGHT - self.game.GROUND.get_height()

        self.pos_x = self.s.WIDTH//4
        self.pos_y = self.s.HEIGHT//2
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]

        self.flash_alpha = 196

    def update(self):
        if self.s.is_bird_moving is True:
            # checks whether conditions are met to gain a point
            self.game.gain_point()
            if self.s.is_bird_ascending is False:
                # if the ascending sequence is terminated, start descending
                self.descend()
            elif self.s.is_bird_ascending is True:
                # if space is pressed, start ascending
                self.ascend()
        elif self.s.is_bird_moving is False and self.game.collision is True:
            # initialize collision sequence
            self.hit()

        self.animate()

    def hit(self):
        # ascend a bird when hit and then let it fall on the ground without animating its wings
        if self.up_collision_factor > 0:
            self.rect.y -= self.up_collision_factor
            self.up_collision_factor -= 0.5
        else:
            if self.rect.bottom < self.ground_height:
                self.rect.y += self.down_collision_factor
                self.down_collision_factor += 0.4
                if self.rect.bottom + self.down_factor > self.ground_height:
                    self.rect.bottom = self.ground_height
                    self.s.can_restart = True

    def ascend(self):
        if self.up_factor >= 1:
            self.rect.y -= self.up_factor if self.rect.y > 0 else 0
            self.up_factor -= 0.5
            if self.rect.y - self.up_factor <= 0:
                self.rect.y = 0
        else:
            self.down_factor = self.init_down_factor
            self.up_factor = self.init_up_factor
            self.s.is_bird_ascending = False

    def descend(self):
        self.rect.y += self.down_factor if (self.rect.bottom < self.ground_height) else 0
        self.down_factor += 0.4
        if self.rect.bottom + self.down_factor > self.ground_height:
            self.rect.bottom = self.ground_height

    def animate(self):
        # iterate through a list if images to animate a sprite
        if self.s.is_bird_animating is True:
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

    def initialize_ascend(self):
        # initialize flags and values for ascending
        self.s.is_bird_moving = True
        self.s.is_bird_ascending = True
        self.up_factor = self.init_up_factor