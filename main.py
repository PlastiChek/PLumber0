import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
PIPE_SIZE = 100
FPS = 60
WHITE = (255, 255, 255)

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
fon = pygame.image.load('data/top-view-soil (1).jpg')
background_image = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT))

pipe_images = [pygame.transform.scale(img, (PIPE_SIZE, PIPE_SIZE)) for img in pipe_images]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Трубопроводчик')


def render_map(map_data, pipe_images):
    pipe_dict = {
        '@': pipe_images[3],  # ПОВОРОТ ЛЕВОНИЗ
        '%': pipe_images[5],  # ПОВОРОТ ПРАВОВВЕРХ
        ':': pipe_images[2],  # ПОВОРОТ ЛЕВОВВЕРХ
        '*': pipe_images[4],  # ПОВОРОТ ПРАВОНИЗ
        '!': pipe_images[7],  # КОНЕЦ ПОТОКА
        '-': pipe_images[0],  # ПОТОК ГОРИЗОНТ
        '/': pipe_images[1],  # ПОТОК ВЕРТИК
        '$': pipe_images[6],  # НАЧАЛО ПОТОКА
    }

    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell in pipe_dict:
                screen.blit(pipe_dict[cell], (j * PIPE_SIZE, i * PIPE_SIZE))


def load_map(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))
    # for i in range(4):
    #     for j in range(8):
    #         screen.blit(pipe_images[j], ((j) * 100, (i) * 100))

    map_data = load_map('LVL3_MAP')
    render_map(map_data, pipe_images)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
