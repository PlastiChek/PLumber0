import pygame
import sys
import random
import time


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    first_line = "Правила игры"
    intro_text = ["Нажимайте левой кнопкой мышки",
                  "на трубу, чтобы её повернуть"]

    screen.blit(start_background, (0, 0))
    screen.blit(metal_plate, (120, 90))
    font = pygame.font.Font(None, 60)
    string_rendered = font.render(first_line, 1, pygame.Color(WHITE))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 250
    text_coord = 100
    intro_rect.top = text_coord
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 40)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(WHITE))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord + 150
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                channel = sound.play()
                return
        if pygame.mouse.get_focused():
            pygame.mouse.set_cursor((0, 0), cursor)
        pygame.display.flip()
        clock.tick(FPS)


def load_map(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [list(line.strip()) for line in file]


def save_map(filename, map_data):
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(''.join(row) + '\n' for row in map_data)


def restore_original_maps():
    original_files = ['data/levels_data/LVL1_MAP_ORIGINAL', 'data/levels_data/LVL2_MAP_ORIGINAL',
                      'data/levels_data/LVL3_MAP_ORIGINAL']
    current_files = ['data/levels_data/LVL1_MAP', 'data/levels_data/LVL2_MAP', 'data/levels_data/LVL3_MAP']

    for original, current in zip(original_files, current_files):
        with open(original, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(current, 'w', encoding='utf-8') as dest:
            dest.write(content)


def start_checking(map_data):
    for i in range(len(map_data)):
        for j in range(len(map_data[i])):
            if map_data[i][j] == '$':
                return check_water(i, j, 1)


def check_water(x, y, rotation):
    try:
        if rotation == 4:
            return win_sequence()
        elif rotation == 0:
            next_pipe = map_data[x - 1][y]
            rotations = {
                '@': 3,
                '/': 0,
                '*': 1,
            }
            return check_water(x - 1, y, rotations[next_pipe])
        elif rotation == 1:
            next_pipe = map_data[x][y + 1]
            rotations = {
                ':': 0,
                '-': 1,
                '@': 2,
                '!': 4
            }
            return check_water(x, y + 1, rotations[next_pipe])
        elif rotation == 2:
            next_pipe = map_data[x + 1][y]
            rotations = {
                '%': 1,
                '/': 2,
                ':': 3
            }
            return check_water(x + 1, y, rotations[next_pipe])
        elif rotation == 3:
            next_pipe = map_data[x][y - 1]
            rotations = {
                '*': 2,
                '-': 3,
                '%': 0
            }
            return check_water(x, y - 1, rotations[next_pipe])
    except KeyError:
        return
    except IndexError:
        return


def win_sequence():
    channel = win_sound.play()
    start_time = time.time()
    while time.time() - start_time < 3:
        screen.blit(background_image, (0, 0))
        render_map(map_data, pipe_images)

        cur_time = time.time() - start_time
        if int(cur_time * 2) % 2 == 0:
            screen.blit(shine_1, (0, 0))
        else:
            screen.blit(shine_2, (0, 0))

        screen.blit(win, (100, 100))

        pygame.display.flip()
        pygame.time.delay(500)

    return True


def check_button_click(pos):
    if 130 <= pos[0] <= 320 and 410 <= pos[1] <= 570:
        return 'data/levels_data/LVL1_MAP'
    elif 350 <= pos[0] <= 540 and 410 <= pos[1] <= 570:
        return 'data/levels_data/LVL2_MAP'
    elif 760 >= pos[0] >= 570 >= pos[1] >= 410:
        return 'data/levels_data/LVL3_MAP'
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

    pygame.draw.rect(screen, (211, 222, 237), (120, 400, 210, 180), 0)
    pygame.draw.rect(screen, (189, 189, 189), (340, 400, 210, 180), 0)
    pygame.draw.rect(screen, (110, 110, 110), (560, 400, 210, 180), 0)

    screen.blit(level1_intro, (130, 410))
    screen.blit(level2_intro, (350, 410))
    screen.blit(level3_intro, (570, 410))

    screen.blit(text_lvl1, (140, 420))
    screen.blit(text_lvl2, (360, 420))
    screen.blit(text_lvl3, (580, 420))


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    PIPE_SIZE = 100
    FPS = 60
    BROWN = (77, 34, 14)
    WHITE = (255, 255, 255)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Трубопроводчик')
    clock = pygame.time.Clock()

    pipe_images = [
        pygame.image.load('data/assets/straight_pipe_90.png'),
        pygame.image.load('data/assets/straight_pipe_0.png'),
        pygame.image.load('data/assets/corner_pipe_270.png'),
        pygame.image.load('data/assets/corner_pipe_180.png'),
        pygame.image.load('data/assets/corner_pipe_90.png'),
        pygame.image.load('data/assets/corner_pipe_0.png'),
        pygame.image.load('data/assets/plumb_start.png'),
        pygame.image.load('data/assets/plumb_end.png')
    ]
    fon = pygame.image.load('data/assets/background.jpg')
    start_bg = pygame.image.load('data/assets/start_background.jpg')
    cursor = pygame.image.load('data/assets/wrench.png')
    metal_plate = pygame.image.load('data/assets/metal_plate.jpg')
    win = pygame.image.load('data/assets/winner.png')
    shine_1 = pygame.image.load('data/assets/shine1.png')
    shine_2 = pygame.image.load('data/assets/shine2.png')
    background_image = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT))
    start_background = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.init()
    sound = pygame.mixer.Sound('data/assets/click_sound.mp3')
    win_sound = pygame.mixer.Sound('data/assets/win_sound.mp3')

    level1_intro = pygame.image.load('data/assets/level1.0.png')
    level2_intro = pygame.image.load('data/assets/level2.0.png')
    level3_intro = pygame.image.load('data/assets/level3.0.png')

    start_screen()

    pipe_images = [pygame.transform.scale(img, (PIPE_SIZE, PIPE_SIZE)) for img in pipe_images]

    font = pygame.font.Font(None, 70)
    text_lvl1 = font.render('Level 1', True, WHITE)
    text_lvl2 = font.render('Level 2', True, WHITE)
    text_lvl3 = font.render('Level 3', True, WHITE)

    current_map_file = 'data/levels_data/LVL1_MAP'
    running = True
    level_complete = False
    map_data = load_map(current_map_file)
    randomize_pipes(map_data)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # левая кнопка мыши
                    row, col = get_clicked_pipe(event.pos)
                    channel = sound.play()
                    if 0 <= row < len(map_data) and 0 <= col < len(map_data[row]):
                        map_data[row][col] = rotate_pipe(map_data[row][col])
                        if not level_complete:
                            level_complete = start_checking(map_data)

                new_map = check_button_click(event.pos)
                if new_map:
                    save_map(current_map_file, map_data)  # сохраняем текущую карту перед загрузкой новой
                    current_map_file = new_map
                    map_data = load_map(current_map_file)
                    randomize_pipes(map_data)  # случайное поворачивание труб при загрузке нового уровня
                    level_complete = False
        if pygame.mouse.get_focused():
            pygame.mouse.set_cursor((0, 0), cursor)

        screen.blit(background_image, (0, 0))
        render_map(map_data, pipe_images)

        pygame.display.flip()
        clock.tick(FPS)
    restore_original_maps()
    terminate()
