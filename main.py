import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
PIPE_SIZE = 100
FPS = 60

pipe_images = [
    pygame.image.load('data/plumb1 (1).png'),
    pygame.image.load('data/plumb6.png'),
    pygame.image.load('data/plumb2 (1).png'),
    pygame.image.load('data/plumb3 (1).png'),
    pygame.image.load('data/plumb4 (1).png'),
    pygame.image.load('data/plumb5 (1).png'),
    pygame.image.load('data/plumb_start.png'),
    pygame.image.load('data/plumb_end.png')
]

for _ in range(len(pipe_images)):
    pipe_images[_].set_colorkey((255, 255, 255))

fon = pygame.image.load('data/top-view-soil (1).jpg')
background_image = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT))

pipe_images = [pygame.transform.scale(img, (PIPE_SIZE, PIPE_SIZE)) for img in pipe_images]

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Трубопроводчик')





clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))
    for i in range(4):
        for j in range(6):
            screen.blit(pipe_images[j + 2], ((j) * 100, (i) * 100))


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
