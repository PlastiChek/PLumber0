import pygame
import sys
import random


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(WHITE))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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


#TODO: функция вызывает себя, пока не найдёт конец трубы
#def check_water(map_data: list):
#    for i in range(len(map_data)):
#        for j in range(len(map_data[i])):
#            if map_data[i][j] == '$':
#                x = j
#                y = i
#    if map_data[x + 1, y] == '@' or map_data[x + 1, y] == ':' or map_data[x + 1, y] == '-':
#        pass


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

    pygame.draw.rect(screen, (0, 128, 128), (130, 410, 190, 160), 0)
    pygame.draw.rect(screen, (127, 255, 212), (350, 410, 190, 160), 0)
    pygame.draw.rect(screen, (0, 191, 255), (570, 410, 190, 160), 0)

    screen.blit(text_lvl1, (140, 420))
    screen.blit(text_lvl2, (360, 420))
    screen.blit(text_lvl3, (580, 420))


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    PIPE_SIZE = 100
    FPS = 60
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
    cursor = pygame.image.load('data/assets/wrench.png')
    background_image = pygame.transform.scale(fon, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.mixer.init()
    sound = pygame.mixer.Sound('data/assets/test_sound.mp3')

    start_screen()

    pipe_images = [pygame.transform.scale(img, (PIPE_SIZE, PIPE_SIZE)) for img in pipe_images]

    font = pygame.font.Font(None, 70)
    text_lvl1 = font.render('Level 1', True, WHITE)
    text_lvl2 = font.render('Level 2', True, WHITE)
    text_lvl3 = font.render('Level 3', True, WHITE)

    current_map_file = 'data/levels_data/LVL1_MAP'
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
                    channel = sound.play()
                    if 0 <= row < len(map_data) and 0 <= col < len(map_data[row]):
                        map_data[row][col] = rotate_pipe(map_data[row][col])

                new_map = check_button_click(event.pos)
                if new_map:
                    save_map(current_map_file, map_data)  # сохраняем текущую карту перед загрузкой новой
                    current_map_file = new_map
                    map_data = load_map(current_map_file)
                    randomize_pipes(map_data)  # случайное поворачивание труб при загрузке нового уровня
            if pygame.mouse.get_focused():
                pygame.mouse.set_cursor((0, 0), cursor)
        screen.blit(background_image, (0, 0))
        render_map(map_data, pipe_images)

        pygame.display.flip()
        clock.tick(FPS)
    restore_original_maps()
    terminate()
