import sys
import pygame
import os
import random
from collections import deque


class Button:
    def __init__(self, text, x, y, w, h, callback, enabled=True):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.enabled = enabled

    def draw(self, surf):
        color = GREEN if self.enabled else (100, 100, 100)
        pygame.draw.rect(surf, color, self.rect)
        txt = font.render(self.text, True, BLACK)
        surf.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                        self.rect.centery - txt.get_height() // 2))

    def click(self, pos):
        if self.enabled and self.rect.collidepoint(pos):
            self.callback()


class Menu:
    def __init__(self):
        self.state = "menu"
        self.buttons = []
        self.max_level_unlocked = 1
        self.infinite_mode_unlocked = False
        self.current_map = None
        self.create_buttons()

    def create_buttons(self):
        self.buttons.clear()
        if self.state == "menu":
            self.buttons.append(Button("Начать игру", WIDTH // 2 - 100,
                                       200, 200, 50, self.start_level_select))
            self.buttons.append(Button("Помощь", WIDTH // 2 - 100,
                                       300, 200, 50, self.show_help))
            self.buttons.append(Button("Выход", WIDTH // 2 - 100,
                                       400, 200, 50, terminate))
        elif self.state == "level_select":
            y = 150
            for lvl in range(1, 5):
                enabled = (lvl <= self.max_level_unlocked)
                self.buttons.append(Button(f"Уровень {lvl}",
                                           WIDTH // 2 - 100, y, 200, 50,
                                           lambda l=lvl: self.load_level(l), enabled))
                y += 70
            self.buttons.append(Button("Бесконечный режим",
                                       WIDTH // 2 - 100, y, 200, 50,
                                       self.load_infinite_mode, self.infinite_mode_unlocked))
            y += 70
            self.buttons.append(Button("Назад",
                                       WIDTH // 2 - 100, y, 200, 50,
                                       self.back_to_menu))
        elif self.state == "help":
            self.buttons.append(Button("Назад",
                                       WIDTH // 2 - 100, HEIGHT - 80, 200, 50,
                                       self.back_to_menu))

    def start_level_select(self):
        self.state = "level_select"
        self.create_buttons()

    def show_help(self):
        self.state = "help"
        self.create_buttons()

    def back_to_menu(self):
        pygame.mixer.music.stop()
        self.state = "menu"
        self.update_window_size()
        self.create_buttons()

    def load_level(self, level):
        print(f"[DEBUG] Запущен уровень {level}")
        if level < 4:
            pygame.mixer.music.load(os.path.join(DATA_DIR, "music.mp3"))
        else:
            pygame.mixer.music.load(os.path.join(DATA_DIR, "secret_music.mp3"))
        pygame.mixer.music.play(-1)
        if level == 5:
            self.current_map = Map(10, filename=None, level=level)  # бесконечный режим
        else:
            filename = f'lvl{level}.txt'
            self.current_map = Map(8, filename=filename, level=level)
        self.state = "level"
        self.update_window_size()

        enemy_sprites.empty()
        tower_sprites.empty()

    def load_infinite_mode(self):
        global screen, WIDTH, HEIGHT
        print("[DEBUG] Запущен бесконечный режим")
        pygame.mixer.music.load(os.path.join(DATA_DIR, "secret_music.mp3"))
        pygame.mixer.music.play(-1)

        grid_size = 10
        self.current_map = Map(grid_size, filename=None, level=5)
        WIDTH, HEIGHT = grid_size * 64, grid_size * 64
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.state = "level"
        self.buttons.clear()
        enemy_sprites.empty()
        tower_sprites.empty()

    def update_window_size(self):
        global screen, WIDTH, HEIGHT
        if self.state == "level" and self.current_map:
            WIDTH = HEIGHT = self.current_map.grid_size * self.current_map.cell_size
        else:
            WIDTH, HEIGHT = 704, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def draw(self):
        screen.fill((50, 50, 80))

        if self.state == "level" and self.current_map:
            self.current_map.draw(screen)
            return  # Не рисуем кнопки в уровне

        if self.state == "menu":
            title = font_big.render("Главное меню", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        elif self.state == "level_select":
            title = font_big.render("Выберите уровень", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        elif self.state == "help":
            title = font_big.render("Помощь", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            help_lines = [
                "1 — Построить/улучшить лучника (10 монет)",
                "Лучники стреляют только по глазам",
                "2 — Построить/улучшить мага (10 монет)",
                "Маги стреляют только по скелетам",
                "Максимальный уровень башен — 3",
                "Игрок строит башни на своей клетке",
                "Башни нельзя строить на дорогах и деревьях",
                "Управление на стрелки или WASD",
                "ESC — выход в меню"
            ]
            y = 150
            for line in help_lines:
                txt = font.render(line, True, WHITE)
                screen.blit(txt, (50, y))
                y += 30

        for btn in self.buttons:
            btn.draw(screen)

    def handle_event(self, event):
        if self.state != "level":
            if event.type == pygame.MOUSEBUTTONUP:
                for btn in self.buttons:
                    if btn.enabled and btn.rect.collidepoint(event.pos):
                        btn.click(event.pos)
                        break
        elif event.type == pygame.KEYDOWN and self.state == "level" and self.current_map:
            player = self.current_map.player
            if event.key in (pygame.K_w, pygame.K_UP):
                player.move(-1, 0)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                player.move(1, 0)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                player.move(0, -1)
                player.facing_right = False  # поворот влево
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                player.move(0, 1)
                player.facing_right = True  # поворот вправо
            elif event.key == pygame.K_1:
                player.build_tower("archer")
            elif event.key == pygame.K_2:
                player.build_tower("wizard")


class Map:
    def __init__(self, size, filename=None, level=1):
        self.cell_size = 64
        self.grid_size = size
        self.surface = pygame.Surface((self.grid_size * self.cell_size,
                                       self.grid_size * self.cell_size))
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.template = [[None for _ in range(size)] for _ in range(size)]
        self.filename = filename
        self.level = level
        self.path = []

        self.last_spawn_time = 0

        back_sprites.empty()

        if filename:
            self.load_from_file(filename)
        else:
            self.generate_random_map()

        self.player = Player(self)

        self.enemies = []
        # Стартовое здоровье и монеты в зависимости от уровня
        start_values = {
            1: (5, 10),
            2: (5, 20),
            3: (10, 30),
            4: (10, 40),
            5: (20, 50)
        }
        self.base_health, starting_coins = start_values.get(self.level, (10, 10))
        self.player.coins = starting_coins
        self.last_wave_time = 0
        self.spawn_index = 0
        self.wave_index = 0
        self.max_enemies_spawned = 0

    def generate_random_map(self):
        # Используем алгоритм твоей генерации пути для создания карты
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Здесь вызываем функции из алгоритма (адаптируем, если нужно)
        start = self.get_start_point_bottom()
        end = self.get_finish_point_top(start[1])

        grid[start[0]][start[1]] = 2
        grid[end[0]][end[1]] = 3

        under_end = (end[0] + 1, end[1])
        if under_end[0] >= self.grid_size:
            under_end = (end[0] - 1, end[1])

        exclude = {start, end, under_end}
        mid_points = self.generate_mid_points(count=6, exclude=exclude)

        ordered_points = [start] + sorted(mid_points, key=lambda p: p[0]) + [under_end, end]
        self.generated_spawn = start

        for i in range(len(ordered_points) - 1):
            self.connect(grid, ordered_points[i], ordered_points[i + 1])

        grid[under_end[0]][under_end[1]] = 1

        path = self.find_path(grid, start, under_end)

        # Оставляем в сетке только клетки пути
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if grid[i][j] == 1 and (i, j) not in path:
                    grid[i][j] = 0

        # Теперь создаём спрайты для отрисовки карты на основе grid
        self.board = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        base_texture, base_rotation = TEXTURE_MAP['..']  # зелёный фон
        base_img = load_image(base_texture)
        base_img = pygame.transform.scale(base_img, (self.cell_size, self.cell_size))

        for x in range(self.grid_size):
            for y in range(self.grid_size):

                sprite = pygame.sprite.Sprite(back_sprites)
                sprite.image = base_img
                sprite.rect = base_img.get_rect()
                sprite.rect.topleft = (y * self.cell_size, x * self.cell_size)
                self.board[x][y] = sprite

        # Отрисовка дороги, старта и финиша
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                code = None

                if grid[x][y] in (1, 2):
                    # Проверка соседей
                    up = x > 0 and grid[x - 1][y] in (1, 2, 3)
                    down = x < self.grid_size - 1 and grid[x + 1][y] in (1, 2, 3)
                    left = y > 0 and grid[x][y - 1] in (1, 2, 3)
                    right = y < self.grid_size - 1 and grid[x][y + 1] in (1, 2, 3)

                    # Особый случай — начальная точка пути
                    if grid[x][y] == 2:
                        # Считаем, что снизу (вниз) есть дорога
                        down = True

                    # Выбор текстуры на основе соседей
                    if (up and down) and not (left or right):
                        code = 'r1'  # вертикальная
                    elif (left and right) and not (up or down):
                        code = 'r2'  # горизонтальная
                    elif up and right and not down and not left:
                        code = 'r3'  # сверху вправо
                    elif left and up and not right and not down:
                        code = 'r4'  # слева вверх
                    elif left and down and not right and not up:
                        code = 'r5'  # слева вниз
                    elif down and right and not left and not up:
                        code = 'r6'  # снизу вправо
                    else:
                        code = 'r1'  # fallback на вертикаль

                elif grid[x][y] == 3:
                    code = 'ca'

                if code:
                    tex_name, rotation = TEXTURE_MAP[code]
                    self.template[x][y] = code
                    if code == 'ca':
                        if x - 1 >= 0:
                            self.template[x - 1][y] = 'ca'
                        if y + 1 < self.grid_size:
                            self.template[x][y + 1] = 'ca'
                        if x - 1 >= 0 and y + 1 < self.grid_size:
                            self.template[x - 1][y + 1] = 'ca'
                    img = load_image(tex_name)
                    if code == 'ca':
                        img = pygame.transform.scale(img, (2 * self.cell_size, 2 * self.cell_size))
                    else:
                        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
                    if rotation:
                        img = pygame.transform.rotate(img, rotation)

                    sprite = pygame.sprite.Sprite(back_sprites)
                    sprite.image = img
                    sprite.rect = img.get_rect()
                    if code == 'ca':
                        sprite.rect.topleft = (y * self.cell_size, (x - 1) * self.cell_size)
                    else:
                        sprite.rect.topleft = (y * self.cell_size, x * self.cell_size)
                    self.board[x][y] = sprite

        self.add_decorations(grid)

        self.path = path
        print(self.template)

    # Реализация вспомогательных функций для генерации пути внутри класса Map:
    def get_start_point_bottom(self):
        return (self.grid_size - 1, random.randint(0, self.grid_size - 1))

    def get_finish_point_top(self, start_y):
        mid = self.grid_size // 2
        if start_y < mid:
            y_range = range(mid, self.grid_size - 1)
        else:
            y_range = range(0, mid)
        y = random.choice(list(y_range))
        return (1, y)

    def generate_mid_points(self, count, exclude):
        points = set()
        while len(points) < count:
            x = random.randint(2, self.grid_size - 3)
            y = random.randint(1, self.grid_size - 2)
            if (x, y) not in exclude:
                points.add((x, y))
        return list(points)

    def connect(self, grid, a, b):
        x1, y1 = a
        x2, y2 = b
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if grid[x1][y] == 0:
                grid[x1][y] = 1
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if grid[x][y2] == 0:
                grid[x][y2] = 1

    def find_path(self, grid, start, goal):
        rows, cols = len(grid), len(grid[0])
        visited = [[False]*cols for _ in range(rows)]
        prev = [[None]*cols for _ in range(rows)]

        queue = deque()
        queue.append(start)
        visited[start[0]][start[1]] = True

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<rows and 0<=ny<cols and not visited[nx][ny] and grid[nx][ny] in (1,3):
                    visited[nx][ny] = True
                    prev[nx][ny] = (x, y)
                    queue.append((nx, ny))

        path = set()
        cur = goal
        while cur and cur != start:
            path.add(cur)
            cur = prev[cur[0]][cur[1]]
        if cur == start:
            path.add(start)
        return path

    def load_from_file(self, filename):
        # Очистить все старые спрайты
        back_sprites.empty()

        path = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Файл {path} не найден.")
        with open(path, encoding='utf-8') as f:
            lines = [line.strip().split() for line in f.readlines() if line.strip()]

        # Выбор базового фона
        default_code = '..' if self.level < 4 else ',,'
        base_texture, base_rotation = TEXTURE_MAP[default_code]
        base_image = load_image(base_texture)
        base_image = pygame.transform.scale(base_image, (self.cell_size, self.cell_size))
        if base_rotation:
            base_image = pygame.transform.rotate(base_image, base_rotation)

        # Заливка карты базовым фоном
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                sprite = pygame.sprite.Sprite(back_sprites)
                sprite.image = base_image
                sprite.rect = base_image.get_rect()
                sprite.rect.topleft = (x * self.cell_size, y * self.cell_size)
                self.board[x][y] = sprite

        # Поверх фона — загрузка объектов из файла
        for y, row in enumerate(lines):
            for x, code in enumerate(row):
                if code not in ("00", "xx", "..", ",,"):
                    self.template[y][x] = code
                    if code == "ca":
                        if y + 1 < self.grid_size:
                            self.template[y + 1][x] = 'ca'
                        if x + 1 < self.grid_size:
                            self.template[y][x + 1] = 'ca'
                        if y + 1 < self.grid_size and x + 1 < self.grid_size:
                            self.template[y + 1][x + 1] = 'ca'

                if code in ("00", "xx", "..", ",,"):
                    continue
                texture_info = TEXTURE_MAP.get(code)
                if not texture_info:
                    continue
                image_name, rotation = texture_info
                img = load_image(image_name)
                if code == "ca":
                    img = pygame.transform.scale(img, (2 * self.cell_size, 2 * self.cell_size))
                else:
                    img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
                if rotation:
                    img = pygame.transform.rotate(img, rotation)
                sprite = pygame.sprite.Sprite(back_sprites)
                sprite.image = img
                sprite.rect = img.get_rect()
                sprite.rect.topleft = (x * self.cell_size, y * self.cell_size)
                self.board[x][y] = sprite
        print(self.template)

    def add_decorations(self, grid):
        decoration_tiles = {
            'b0': "bush.png",  # трава с мхом
            'b1': "bush1.png",  # трава с ягодами
            'h0': "house.png",  # домик с выходом снизу
            'h1': "house1.png",  # домик с выходом справа
            'h2': "house2.png",  # домик с выходом сверху
            'h3': "house3.png",  # домик с выходом слева
            't0': "tree.png",  # дерево с яблоками
            't1': "tree1.png",  # просто дерево
            'wh': "wheat.png",  # пшеница
            'gr': "grass.png"  # трава
        }

        num_decor = random.randint(30, 40)  # немного увеличим количество
        placed_positions = set()

        def is_near_path(x, y):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        if grid[nx][ny] in (1, 2, 3):
                            return True
            return False

        attempts = 0
        max_attempts = 500

        while num_decor > 0 and attempts < max_attempts:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if grid[x][y] == 0 and (x, y) not in placed_positions and not is_near_path(x, y):
                key, img_name = random.choice(list(decoration_tiles.items()))
                img = load_image(img_name)
                img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
                sprite = pygame.sprite.Sprite(back_sprites)
                sprite.image = img
                sprite.rect = img.get_rect()
                sprite.rect.topleft = (y * self.cell_size, x * self.cell_size)
                self.board[x][y] = sprite
                self.template[x][y] = key
                placed_positions.add((x, y))
                num_decor -= 1

            attempts += 1

    def draw_status_bar(self, surf):
        # Иконки
        icon_hp = pygame.transform.scale(load_image("hp.png"), (32, 32))
        icon_coin = pygame.transform.scale(load_image("coin.png"), (32, 32))
        icon_xp = pygame.transform.scale(load_image("xp.png"), (32, 32))

        # Позиции
        y = self.grid_size * self.cell_size - 40
        x_hp = 10
        x_coin = x_hp + 100
        x_xp = x_coin + 100

        # Отображение
        surf.blit(icon_hp, (x_hp, y))
        text_hp = font.render(str(self.base_health), True, (200, 50, 50))
        surf.blit(text_hp, (x_hp + 40, y + 4))

        surf.blit(icon_coin, (x_coin, y))
        text_coin = font.render(str(self.player.coins), True, (230, 230, 0))
        surf.blit(text_coin, (x_coin + 40, y + 4))

        surf.blit(icon_xp, (x_xp, y))
        text_xp = font.render(str(xp), True, (0, 255, 0))
        surf.blit(text_xp, (x_xp + 40, y + 4))

    def update(self):
        current_time = pygame.time.get_ticks()

        # Появление врагов
        level_settings = {
            1: {'eye_hp': 3, 'skel_hp': 6, 'eye_speed': 1.5, 'skel_speed': 1.0, 'count': 10, 'wave_size': 2},
            2: {'eye_hp': 3, 'skel_hp': 6, 'eye_speed': 2.0, 'skel_speed': 1.3, 'count': 15, 'wave_size': 3},
            3: {'eye_hp': 3, 'skel_hp': 6, 'eye_speed': 2.5, 'skel_speed': 1.8, 'count': 20, 'wave_size': 4},
            4: {'eye_hp': 3, 'skel_hp': 6, 'eye_speed': 3.0, 'skel_speed': 2.0, 'count': 25, 'wave_size': 5},
            5: {},  # бесконечный режим
        }

        if self.level < 5:
            conf = level_settings[self.level]
            if self.max_enemies_spawned < conf['count']:
                if self.spawn_index < conf['wave_size']:
                    now = pygame.time.get_ticks()
                    if not self.enemies or self.enemies[-1].moved_enough():
                        if now - self.last_spawn_time >= 500:  # 500 мс между монстрами
                            self.spawn_enemy_wave(conf)
                            self.last_spawn_time = now
                elif current_time - self.last_wave_time > 5000:
                    self.spawn_index = 0
        else:
            if self.spawn_index == 0:
                eye_hp = 3
                skel_hp = 6

                if self.wave_index >= 20:
                    eye_hp += ((self.wave_index - 20) // 5)
                    skel_hp += 2 * ((self.wave_index - 20) // 5)

                self.current_wave_conf = {
                    'eye_hp': eye_hp,
                    'skel_hp': skel_hp,
                    'eye_speed': 1.5 + 0.1 * self.wave_index,
                    'skel_speed': 1.0 + 0.1 * self.wave_index
                }

            wave_size = 2 + self.wave_index // 5
            if self.spawn_index < wave_size:
                now = pygame.time.get_ticks()
                if not self.enemies or self.enemies[-1].moved_enough():
                    if now - self.last_spawn_time >= 500:  # 500 мс между монстрами
                        self.spawn_enemy_wave(self.current_wave_conf)
                        self.last_spawn_time = now
            elif current_time - self.last_wave_time > 5000:
                self.spawn_index = 0
                self.wave_index += 1

        # Обновление врагов
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.reached_base or enemy.hp <= 0:
                global xp
                xp += 50
                self.player.coins += 5
                if enemy.hp <= 0:
                    if enemy.kind == "eye":
                        eye_death_sound.play()
                    else:
                        skell_death_sound.play()
                else:
                    no_hp_sound.play()
                enemy.kill()
                self.enemies.remove(enemy)
                if enemy.reached_base:
                    self.base_health -= 1

        # Победа
        if self.level < 5:
            conf = {
                1: 10, 2: 15, 3: 20, 4: 25
            }
            if self.max_enemies_spawned == conf[self.level] and not self.enemies and self.base_health > 0:
                pygame.mixer.music.stop()
                win_sound.play()
                self.show_end_screen(victory=True)

        # Поражение
        if self.base_health <= 0:
            pygame.mixer.music.stop()
            lose_sound.play()
            self.show_end_screen(victory=False)

    def show_end_screen(self, victory):
        global xp
        screen.fill(WHITE)

        if victory:
            img = load_image("win.png")
            if self.level == menu.max_level_unlocked and menu.max_level_unlocked < 5:
                menu.max_level_unlocked += 1
            if menu.max_level_unlocked == 5:
                menu.infinite_mode_unlocked = True
        else:
            img = load_image("lose.png")
            xp = 0  # сброс опыта

        img = pygame.transform.scale(img, (self.grid_size * self.cell_size, self.grid_size * self.cell_size))
        screen.blit(img, (0, 0))

        # Надпись внизу
        text = font_big.render(f"Вы набрали {xp} очков", True, BLACK)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT - 60))

        pygame.display.flip()
        pygame.time.delay(3000)
        menu.back_to_menu()

    def spawn_enemy_wave(self, conf):
        spawn_points = {
            1: (0, 0),
            2: (7, 2),
            3: (3, 7),
            4: (0, 0)
        }

        if self.level < 5:
            sx, sy = spawn_points[self.level]
        else:
            sx, sy = self.generated_spawn

        tx, ty = next(((x + 1, y) for x in range(self.grid_size)
                       for y in range(self.grid_size)
                       if self.template[x][y] == 'ca'), (0, 0))

        road = self.find_path_from_template((sx, sy), (tx, ty))

        if not road:
            return

        kind = random.choice(["eye", "skel"])
        if kind == "eye":
            enemy = Enemy(self, sx, sy, road, "eye", conf["eye_hp"], conf["eye_speed"])
        else:
            enemy = Enemy(self, sx, sy, road, "skel", conf["skel_hp"], conf["skel_speed"])

        enemy_sprites.add(enemy)
        self.enemies.append(enemy)
        self.spawn_index += 1
        self.max_enemies_spawned += 1
        self.last_wave_time = pygame.time.get_ticks()

    def find_path_from_template(self, start, goal):
        q = deque([start])
        visited = set()
        prev = {}
        visited.add(start)

        while q:
            cx, cy = q.popleft()
            if (cx, cy) == goal:
                break
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if (nx, ny) not in visited:
                        code = self.template[nx][ny]
                        if code and (code.startswith('r') or code == 'br' or (nx, ny) == goal):
                            visited.add((nx, ny))
                            prev[(nx, ny)] = (cx, cy)
                            q.append((nx, ny))

        path = []
        cur = goal
        while cur != start:
            path.append(cur)
            cur = prev.get(cur)
            if cur is None:
                return []  # путь не найден
        path.append(start)
        return path[::-1]

    def draw_wave_number(self, surf):
        if self.level == 5:
            text = font_big.render(f"Волна {self.wave_index + 1}", True, WHITE)
            surf.blit(text, ((WIDTH - text.get_width()) // 2, 10))

    def draw(self, surf):
        surf.fill((30, 30, 30))
        back_sprites.draw(surf)
        self.player.draw(surf)
        tower_sprites.update()
        projectile_sprites.update()
        tower_sprites.draw(surf)
        projectile_sprites.draw(surf)
        for tower in tower_sprites:
            tower.draw_level(surf)
        enemy_sprites.draw(surf)
        for enemy in self.enemies:
            enemy.draw_health(surf)
        self.update()
        self.draw_wave_number(surf)
        self.draw_status_bar(surf)


class Player:
    def __init__(self, map_obj):
        self.map = map_obj
        self.cell_size = map_obj.cell_size
        self.x, self.y = 0, 0  # начальная позиция на сетке
        self.facing_right = True  # по умолчанию вправо
        self.image = pygame.transform.scale(load_image("hero.png"), (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect()
        self.update_rect()
        self.coins = 0

    def update_rect(self):
        self.rect.topleft = (self.y * self.cell_size, self.x * self.cell_size)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.map.grid_size and 0 <= new_y < self.map.grid_size:
            self.x = new_x
            self.y = new_y
            self.update_rect()

    def build_tower(self, tower_type):
        tx, ty = self.x, self.y
        template = self.map.template[tx][ty]
        allowed = template in (None, 'gr', 'b0', 'b1')
        if not allowed:
            return

        existing = [t for t in tower_sprites if t.grid == (tx, ty)]
        if existing:
            tower = existing[0]
            if tower.type == tower_type and tower.level < 3 and self.coins >= 10:
                self.coins -= 10
                tower.level += 1
                tower.damage += 1
        elif self.coins >= 10:
            self.coins -= 10
            Tower(self.map, tx, ty, tower_type)


    def draw(self, surface):
        image = self.image
        if not self.facing_right:
            image = pygame.transform.flip(self.image, True, False)
        surface.blit(image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, map_ref, x, y, path, kind, hp, speed):
        super().__init__()
        self.map = map_ref
        self.kind = kind
        self.image = pygame.transform.scale(load_image("eye.png" if kind == "eye" else "skell.png"), (48, 48))
        self.rect = self.image.get_rect()
        self.cell_size = 64
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.max_hp = hp
        self.hp = hp
        self.reached_base = False
        self.set_position(self.path[0])
        self.pos = pygame.Vector2(self.rect.center)

    def set_position(self, cell):
        self.rect.center = (cell[1] * 64 + 32, cell[0] * 64 + 32)

    def update(self):
        if self.path_index >= len(self.path):
            return

        target_cell = self.path[self.path_index]
        target = pygame.Vector2(target_cell[1] * 64 + 32, target_cell[0] * 64 + 32)
        direction = target - self.pos
        distance = direction.length()

        if distance <= self.speed:
            self.pos = target
            self.rect.center = target
            self.path_index += 1
            if self.path_index >= len(self.path):
                self.reached_base = True
            return

        direction = direction.normalize()
        self.pos += direction * self.speed
        self.rect.center = self.pos

    def draw_health(self, surf):
        x, y = self.rect.centerx, self.rect.top - 10
        width = 32
        height = 6
        ratio = self.hp / self.max_hp
        color = GREEN if ratio > 0.66 else (255, 255, 0) if ratio > 0.33 else (255, 0, 0)
        pygame.draw.rect(surf, BLACK, (x - width // 2, y, width, height))
        pygame.draw.rect(surf, color, (x - width // 2, y, int(width * ratio), height))

        text = pygame.font.Font(None, 20).render(f"{self.hp}/{self.max_hp}", True, WHITE)
        surf.blit(text, (x - text.get_width() // 2, y))

    def moved_enough(self):
        return True  # можно усложнить проверкой расстояния


class Tower(pygame.sprite.Sprite):
    def __init__(self, map_ref, x, y, tower_type):
        super().__init__(tower_sprites)
        self.map = map_ref
        self.grid = (x, y)
        self.type = tower_type
        self.cell_size = map_ref.cell_size
        self.level = 1
        self.damage = 1
        self.base_cooldown = 1000  # мс на 1 уровне
        self.last_shot_time = 0

        img_name = "archer.png" if tower_type == "archer" else "wizard.png"
        self.image = pygame.transform.scale(load_image(img_name), (self.cell_size, self.cell_size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (y * self.cell_size, x * self.cell_size)

    def update(self):
        now = pygame.time.get_ticks()
        cooldown = self.base_cooldown * (1 - 0.1 * (self.level - 1))  # lvl2: 900мс, lvl3: 800мс
        if now - self.last_shot_time < cooldown:
            return

        enemies = self.map.enemies
        in_range = []
        tx, ty = self.grid
        for enemy in enemies:
            ex, ey = enemy.rect.center
            gx, gy = ex // 64, ey // 64
            if abs(tx - gy) <= 1 and abs(ty - gx) <= 1:
                if self.type == "archer" and enemy.kind == "eye":
                    in_range.append(enemy)
                elif self.type == "wizard" and enemy.kind == "skel":
                    in_range.append(enemy)

        # Выбираем цель с учётом избыточного урона
        for enemy in in_range:
            incoming = sum(p.damage for p in projectile_sprites if p.target == enemy)
            if enemy.hp - incoming > 0:
                Projectile(self, enemy)
                self.last_shot_time = now
                if self.type == "archer":
                    arrow_sound.play()
                else:
                    fireball_sound.play()
                break

    def draw_level(self, surf):
        x, y = self.rect.centerx, self.rect.bottom + 2
        font_small = pygame.font.Font(None, 20)
        txt = font_small.render(f"{self.level} lvl", True, WHITE)
        surf.blit(txt, (x - txt.get_width() // 2, y))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, tower, target):
        super().__init__(projectile_sprites)
        self.target = target
        self.speed = 20
        self.damage = tower.damage
        img_name = "arrow.png" if tower.type == "archer" else "fireball.png"
        self.image = pygame.transform.scale(load_image(img_name), (24, 24))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(tower.rect.center)
        self.rect.center = self.pos

    def update(self):
        if not self.target or self.target.hp <= 0:
            self.kill()
            return
        target_pos = pygame.Vector2(self.target.rect.center)
        direction = target_pos - self.pos
        if direction.length() < self.speed:
            self.target.hp -= self.damage
            self.kill()
            return
        direction = direction.normalize()
        self.pos += direction * self.speed
        self.rect.center = self.pos


def terminate():
    global screen
    screen = pygame.display.set_mode((704, 700))
    background_path = os.path.join(DATA_DIR, "thanks_background.png")
    if not os.path.isfile(background_path):
        raise FileNotFoundError(f"Файл {background_path} не найден.")
    background = pygame.image.load(background_path).convert()
    screen.blit(background, (0, 0))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type in (pygame.KEYDOWN,
                                                           pygame.MOUSEBUTTONDOWN):
                waiting = False
    pygame.quit()
    sys.exit()


def load_image(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл {path} не найден.")
    return pygame.image.load(path).convert_alpha()


def main():
    global menu
    menu = Menu()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.back_to_menu()
            else:
                menu.handle_event(event)

        menu.draw()
        pygame.display.flip()
        clock.tick(FPS)


# Путь к папке с текстурами и звуками
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# Словарь текстур
TEXTURE_MAP = {
    '..': ("background.png", 0),  # зелёный фон
    ',,': ("background_scary.png", 0),  # коричневый фон
    'st': ("scary_tree.png", 0),  # сухое дерево
    'sr': ("scary_river.png", 90),  # река с коричневым берегом
    'br': ("bridge.png", 90),  # мост для реки с коричневым берегом
    'r1': ("road.png", 0),  # вертикальная дорога
    'r2': ("road.png", 90),  # горизонтальная дорога
    'r3': ("road1.png", 90),  # поворот сверху вправо
    'r4': ("road1.png", 180),  # поворот слева вверх
    'r5': ("road1.png", 270),  # поворот слева вниз
    'r6': ("road1.png", 0),  # поворот снизу вправо
    'b0': ("bush.png", 0),  # трава с мхом
    'b1': ("bush1.png", 0),  # трава с ягодами
    'ca': ("house big.png", 0),  # база размером 2x2 клетки, вход снизу
    'h0': ("house.png", 0),  # декоративный домик с выходом снизу
    'h1': ("house1.png", 0),  # декоративный домик с выходом справа
    'h2': ("house2.png", 0),  # декоративный домик с выходом сверху
    'h3': ("house3.png", 0),  # декоративный домик с выходом слева
    't0': ("tree.png", 0),  # дерево с яблоками
    't1': ("tree1.png", 0),  # просто дерево
    'wh': ("wheat.png", 0),  # пшеница с подходами со всех четырёх сторон
    'w1': ("river.png", 0),  # вертикальная река
    'w2': ("river.png", 90),  # горизонтальная река
    'w3': ("river1.png", 90),  # река сверху вправо
    'w4': ("river1.png", 180),  # река слева вверх
    'w5': ("river1.png", 270),  # река слева вниз
    'w6': ("river1.png", 0),  # река снизу вправо
    'gr': ("grass.png", 0),  # трава
}

# --- Настройки ---
WIDTH, HEIGHT = 704, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
xp = 0

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Йопики у ворот!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
font_big = pygame.font.Font(None, 64)

# Загрузка звуков
arrow_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "arrow.wav"))
fireball_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "fireball.wav"))
skell_death_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "skell.wav"))
eye_death_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "eye.wav"))
no_hp_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "no_hp.wav"))
lose_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "loseSound.wav"))
win_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, "winSound.wav"))

icon_path = os.path.join(DATA_DIR, "icon.ico")
if not os.path.isfile(icon_path):
    raise FileNotFoundError(f"Файл {icon_path} не найден.")
pygame.display.set_icon(pygame.image.load(icon_path))

enemy_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
tower_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()

if __name__ == "__main__":
    main()
