import pygame as pg


class Ground(pg.sprite.Sprite):

    def __init__(self, game, settings):
        super().__init__()
        self.s = settings
        self.game = game
        self.image = self.game.GROUND

        self.rect = self.image.get_rect()
        self.rect.y = self.s.HEIGHT - self.game.GROUND.get_height()
        self.rect.x = 0

    def update(self):
        if self.s.is_ground_active:
            if self.rect.right <= self.s.WIDTH:
                self.rect.x = 0
            self.rect.x -= self.s.objects_speed
