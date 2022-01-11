import pygame as pg


class Points(pg.sprite.Sprite):

    def __init__(self, settings, current_number, alpha=255, size=0, pos_x=0, pos_y=0):
        super().__init__()
        self.s = settings
        self.current_number = current_number

        self.zero = pg.image.load("assets/images/numbers/0.png")
        self.zero = pg.transform.scale(self.zero, (self.zero.get_width() * (self.s.SCALE/2 + 1),
                                                   self.zero.get_height() * (self.s.SCALE/2 + 1)))
        self.one = pg.image.load("assets/images/numbers/1.png")
        self.one = pg.transform.scale(self.one, (self.zero.get_width(), self.zero.get_height()))
        self.two = pg.image.load("assets/images/numbers/2.png")
        self.two = pg.transform.scale(self.two, (self.zero.get_width(), self.zero.get_height()))
        self.three = pg.image.load("assets/images/numbers/3.png")
        self.three = pg.transform.scale(self.three, (self.zero.get_width(), self.zero.get_height()))
        self.four = pg.image.load("assets/images/numbers/4.png")
        self.four = pg.transform.scale(self.four, (self.zero.get_width(), self.zero.get_height()))
        self.five = pg.image.load("assets/images/numbers/5.png")
        self.five = pg.transform.scale(self.five, (self.zero.get_width(), self.zero.get_height()))
        self.six = pg.image.load("assets/images/numbers/6.png")
        self.six = pg.transform.scale(self.six, (self.zero.get_width(), self.zero.get_height()))
        self.seven = pg.image.load("assets/images/numbers/7.png")
        self.seven = pg.transform.scale(self.seven, (self.zero.get_width(), self.zero.get_height()))
        self.eight = pg.image.load("assets/images/numbers/8.png")
        self.eight = pg.transform.scale(self.eight, (self.zero.get_width(), self.zero.get_height()))
        self.nine = pg.image.load("assets/images/numbers/9.png")
        self.nine = pg.transform.scale(self.nine, (self.zero.get_width(), self.zero.get_height()))

        self.s_zero = pg.image.load('assets/images/numbers/0-small.png')
        self.s_zero = pg.transform.scale(self.s_zero, (self.s_zero.get_width() * self.s.SCALE,
                                                       self.s_zero.get_height() * self.s.SCALE))
        self.s_one = pg.image.load('assets/images/numbers/1-small.png')
        self.s_one = pg.transform.scale(self.s_one, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_two = pg.image.load('assets/images/numbers/2-small.png')
        self.s_two = pg.transform.scale(self.s_two, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_three = pg.image.load('assets/images/numbers/3-small.png')
        self.s_three = pg.transform.scale(self.s_three, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_four = pg.image.load('assets/images/numbers/4-small.png')
        self.s_four = pg.transform.scale(self.s_four, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_five = pg.image.load('assets/images/numbers/5-small.png')
        self.s_five = pg.transform.scale(self.s_five, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_six = pg.image.load('assets/images/numbers/6-small.png')
        self.s_six = pg.transform.scale(self.s_six, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_seven = pg.image.load('assets/images/numbers/7-small.png')
        self.s_seven = pg.transform.scale(self.s_seven, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_eight = pg.image.load('assets/images/numbers/8-small.png')
        self.s_eight = pg.transform.scale(self.s_eight, (self.s_zero.get_width(), self.s_zero.get_height()))
        self.s_nine = pg.image.load('assets/images/numbers/9-small.png')
        self.s_nine = pg.transform.scale(self.s_nine, (self.s_zero.get_width(), self.s_zero.get_height()))

        if size == 0:
            self.images_list = [self.zero, self.one, self.two, self.three, self.four, self.five, self.six, self.seven,
                                self.eight, self.nine]
        else:
            self.images_list = [self.s_zero, self.s_one, self.s_two, self.s_three, self.s_four,
                                self.s_five, self.s_six, self.s_seven, self.s_eight, self.s_nine]

        self.image = self.images_list[self.current_number]
        self.image.convert_alpha()
        self.image.set_alpha(alpha)
        self.rect = self.image.get_rect()

        if size == 0:
            self.rect.centery = self.s.HEIGHT//10
            self.rect.centerx = self.s.WIDTH//2
        else:
            self.rect.centerx = pos_x
            self.rect.centery = pos_y

        self.w = self.zero.get_width()

    def update(self, number=0, alpha=0, pos_x=0):
        self.current_number = number
        self.image = self.images_list[self.current_number]
        self.image.convert_alpha()
        self.image.set_alpha(alpha)
        self.rect.centerx = pos_x