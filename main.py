import pygame
import sys
import random


def load_map(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [list(line.strip()) for line in file]


def save_map(filename, map_data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(''.join(row) + '\n' for row in map_data)


def restore_original_maps():
    original_files = ['levels_data/LVL1_MAP_ORIGINAL', 'levels_data/LVL2_MAP_ORIGINAL', 'levels_data/LVL3_MAP_ORIGINAL']
    current_files = ['levels_data/LVL1_MAP', 'levels_data/LVL2_MAP', 'levels_data/LVL3_MAP']

    for original, current in zip(original_files, current_files):
        with open(original, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(current, 'w', encoding='utf-8') as dest:
            dest.write(content)


def check_button_click(pos):
    if 130 <= pos[0] <= 320 and 410 <= pos[1] <= 570:
        return 'levels_data/LVL1_MAP'
    elif 350 <= pos[0] <= 540 and 410 <= pos[1] <= 570:
        return 'levels_data/LVL2_MAP'
    elif 570 <= pos[0] <= 760 and 410 <= pos[1] <= 570:
        return 'levels_data/LVL3_MAP'
    return None


def get_clicked_pipe(pos):
    x, y = pos
    row, col = y // PIPE_SIZE, x // PIPE_SIZE
    return row, col


def rotate_pipe(pipe):
    rotation_map = {
        '-': '/',  # горизонт -> вертикаль
        '/': '-',  # вертикаль -> горизонт
        '@': ':',  # поворот левониз -> левовверх
        ':': '%',  # поворот левовверх -> правовверх
        '%': '*',  # поворот правовверх -> правониз
        '*': '@'  # поворот правониз -> левониз
    }
    return rotation_map.get(pipe, pipe)  # вернуть обновленный символ или оставить без изменений


def randomize_pipes(map_data):
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell in ('-', '/', '@', '%', '*', ':'):
                rotations = random.randint(0, 3)
                for _ in range(rotations):
                    cell = rotate_pipe(cell)
                map_data[i][j] = cell


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


current_map_file = 'levels_data/LVL1_MAP'
clock = pygame.time.Clock()
running = True
map_data = load_map(current_map_file)
randomize_pipes(map_data)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                row, col = get_clicked_pipe(event.pos)
                if 0 <= row < len(map_data) and 0 <= col < len(map_data[row]):
                    map_data[row][col] = rotate_pipe(map_data[row][col])

            new_map = check_button_click(event.pos)
            if new_map:
                save_map(current_map_file, map_data)  # сохраняем текущую карту перед загрузкой новой
                current_map_file = new_map
                map_data = load_map(current_map_file)
                randomize_pipes(map_data)  # случайное поворачивание труб при загрузке нового уровня

    screen.blit(background_image, (0, 0))
    render_map(map_data, pipe_images)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
restore_original_maps()
sys.exit()
