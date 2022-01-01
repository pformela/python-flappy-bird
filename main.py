import pygame
import sys

SCALE = 3
WIDTH = SCALE * 144
HEIGHT = SCALE * 256

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

BACKGROUND = pygame.transform.scale(pygame.image.load('assets/images/background.png'), (WIDTH, HEIGHT))
GROUND = pygame.image.load('assets/images/ground.png')
GROUND = pygame.transform.scale(GROUND, (GROUND.get_width() * 3, GROUND.get_height() * 3))
GRASS = pygame.image.load('assets/images/grass.png')
GRASS = pygame.transform.scale(GRASS, (GRASS.get_width() * 3, GRASS.get_height() * 3))
BIRD = pygame.image.load('assets/images/bird1.png')
BIRD = pygame.transform.scale(BIRD, (BIRD.get_width() * 3, BIRD.get_height() * 3))

clock = pygame.time.Clock()


# def handle_bird_movement():

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = BIRD
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH//4, HEIGHT//2]

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))


def main():

    pygame.init()
    bird = Bird()
    bird_group = pygame.sprite.Group()
    bird_group.add(bird)
    running = True

    while running:

        WIN.fill((255, 255, 255))
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(GROUND, (0, HEIGHT - GROUND.get_height()))
        WIN.blit(GRASS, (0, HEIGHT - GROUND.get_height() - GRASS.get_height()))
        bird_group.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
