import pygame as pg


class Pipe(pg.sprite.Sprite):

    def __init__(self, pos_x, pos_y, settings):
        super().__init__()
        self.s = settings

        self.image = pg.image.load('assets/images/pipes.png')
        self.width, self.height = self.image.get_width(), self.image.get_height()
        self.image = pg.transform.scale(self.image, (self.width * self.s.SCALE, self.height * self.s.SCALE))
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

        self.rect.x, self.rect.y = pos_x, pos_y

    def update(self):
        self.rect.x -= self.s.objects_speed