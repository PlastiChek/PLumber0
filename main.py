import pygame
import sys


def load_map(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def check_button_click(pos):
    if 130 <= pos[0] <= 320 and 410 <= pos[1] <= 570:
        return 'LVL1_MAP'
    elif 350 <= pos[0] <= 540 and 410 <= pos[1] <= 570:
        return 'LVL2_MAP'
    elif 570 <= pos[0] <= 760 and 410 <= pos[1] <= 570:
        return 'LVL3_MAP'
    return None


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
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

font = pygame.font.Font(None, 70)
text_lvl1 = font.render('Level 1', True, WHITE)
text_lvl2 = font.render('Level 2', True, WHITE)
text_lvl3 = font.render('Level 3', True, WHITE)


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

    pygame.draw.rect(screen, (0, 128, 128), (130, 410, 190, 160), 0)
    pygame.draw.rect(screen, (127, 255, 212), (350, 410, 190, 160), 0)
    pygame.draw.rect(screen, (0, 191, 255), (570, 410, 190, 160), 0)

    screen.blit(text_lvl1, (140, 420))
    screen.blit(text_lvl2, (360, 420))
    screen.blit(text_lvl3, (580, 420))


current_map_file = 'LVL3_MAP'
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_map = check_button_click(event.pos)
            if new_map:
                current_map_file = new_map

    screen.blit(background_image, (0, 0))
    map_data = load_map(current_map_file)
    render_map(map_data, pipe_images)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
