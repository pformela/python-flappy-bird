class Settings:

    def __init__(self):
        self.SCALE = 3
        self.WIDTH = self.SCALE * 144
        self.HEIGHT = self.SCALE * 256

        self.FPS = 60

        self.game_running = True
        self.move_pipes = False
        self.move_ground = True
        self.is_ground_active = True
        self.is_bird_moving = False
        self.is_bird_ascending = False
        self.is_bird_animating = True
        self.can_restart = False

        self.min_pipe_y = -140 * self.SCALE
        self.max_pipe_y = -30 * self.SCALE
        self.pipe_distance = 83 * self.SCALE
        self.objects_speed = 1 * self.SCALE
        self.new_x = self.WIDTH - self.pipe_distance
