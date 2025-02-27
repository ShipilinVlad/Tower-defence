import os
import sys
import pygame
import random


class Monster:
    pass


class Tower:
    pass


class Board:
    def __init__(self):
        self.board = [[no_sprite] * n for _ in range(n)]
        self.left = 10
        self.top = 10
        self.cell_size = 16

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, sprites_group, screen_to_draw):
        for i in range(n):
            for j in range(n):
                cell = self.board[i][j]
                coord = (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size)
                try:
                    if cell:
                        cell.rect.x, cell.rect.y = coord[0], coord[1]
                except AttributeError:
                    pass
        sprites_group.draw(screen_to_draw)

    def move(self, x, y, move_x, move_y, sprite):
        self.board[y][x] = no_sprite
        self.board[y + move_y][x + move_x] = sprite

    def fill(self, text_lvl):
        for i in range(n):
            for j in range(n):
                if text_lvl[i][j] == '00' or text_lvl[i][j] == 'xx':
                    continue
                elem = pygame.sprite.Sprite(back_sprites)
                if text_lvl[i][j] == '..':
                    elem.image = pygame.transform.scale(load_image("background.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == ',,':
                    elem.image = pygame.transform.scale(load_image("background_scary.png"),
                                                        (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == 'st':
                    elem.image = pygame.transform.scale(load_image("scary_tree.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == 'sr':
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("scary_river.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == 'br':
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("bridge.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == "r1":
                    elem.image = pygame.transform.scale(load_image("road.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "r2":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("road.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == "r3":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("road1.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == "r4":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("road1.png"), (self.cell_size, self.cell_size)), 180)
                elif text_lvl[i][j] == "r5":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("road1.png"), (self.cell_size, self.cell_size)), 270)
                elif text_lvl[i][j] == "r6":
                    elem.image = pygame.transform.scale(load_image("road1.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "b0":
                    elem.image = pygame.transform.scale(load_image("bush.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "b1":
                    elem.image = pygame.transform.scale(load_image("bush1.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "ca":
                    elem.image = pygame.transform.scale(load_image("house big.png"),
                                                        (2 * self.cell_size, 2 * self.cell_size))
                elif text_lvl[i][j] == "h0":
                    elem.image = pygame.transform.scale(load_image("house.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "h1":
                    elem.image = pygame.transform.scale(load_image("house1.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "h2":
                    elem.image = pygame.transform.scale(load_image("house2.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "h3":
                    elem.image = pygame.transform.scale(load_image("house3.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "t0":
                    elem.image = pygame.transform.scale(load_image("tree.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "t1":
                    elem.image = pygame.transform.scale(load_image("tree1.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "wh":
                    elem.image = pygame.transform.scale(load_image("wheat.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "w1":
                    elem.image = pygame.transform.scale(load_image("river.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "w2":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("river.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == "w3":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("river1.png"), (self.cell_size, self.cell_size)), 90)
                elif text_lvl[i][j] == "w4":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("river1.png"), (self.cell_size, self.cell_size)), 180)
                elif text_lvl[i][j] == "w5":
                    elem.image = pygame.transform.rotate(
                        pygame.transform.scale(load_image("river1.png"), (self.cell_size, self.cell_size)), 270)
                elif text_lvl[i][j] == "w6":
                    elem.image = pygame.transform.scale(load_image("river1.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "gr":
                    elem.image = pygame.transform.scale(load_image("grass.png"), (self.cell_size, self.cell_size))
                elem.rect = elem.image.get_rect()
                self.board[i][j] = elem


class Player:
    pass


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level = [line.split() for line in mapFile]
    return level


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((255, 255, 255))
    start_end_group.empty()
    start_sprite = pygame.sprite.Sprite(start_end_group)
    start_sprite.image = load_image('start.png')
    start_sprite.rect = start_sprite.image.get_rect()
    start_sprite.rect.x, start_sprite.rect.y = 0, 0
    note_surface = pygame.Surface((700, 120))
    note_surface.fill((255, 255, 255))
    note_font = pygame.font.Font(None, 50)
    note_text = note_font.render(f"Нажмите 1, 2 или 3 для выбора уровня", True, pygame.color.Color('black'))
    note_text_x = 0
    note_text_y = 0
    note_surface.blit(note_text, (note_text_x, note_text_y))

    note_text2 = note_font.render(f"Нажмите Esc для выхода", True, pygame.color.Color('black'))
    note_text_x2 = 0
    note_text_y2 = 50
    note_surface.blit(note_text2, (note_text_x2, note_text_y2))

    screen.blit(note_surface, (15, 590))
    while True:
        for event_start in pygame.event.get():
            if event_start.type == pygame.QUIT:
                terminate()
            elif event_start.type == pygame.KEYDOWN:
                if event_start.key == pygame.K_1:
                    if current_music[0] != 'normal':
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/music.mp3')
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(-1)
                        current_music[0] = 'normal'
                    return levels['first']
                elif event_start.key == pygame.K_2:
                    if current_music[0] != 'normal':
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/music.mp3')
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(-1)
                        current_music[0] = 'normal'
                    return levels['second']
                elif event_start.key == pygame.K_3:
                    if current_music[0] != 'normal':
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/music.mp3')
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(-1)
                        current_music[0] = 'normal'
                    return levels['third']
                elif event_start.key == pygame.K_4:
                    if current_music[0] == 'normal':
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/secret_music.mp3')
                        pygame.mixer.music.set_volume(0.7)
                        pygame.mixer.music.play(-1)
                        current_music[0] = 'secret'
                    return levels['fourth']
                elif event_start.key == pygame.K_ESCAPE:
                    thx_for_game_surface = pygame.Surface((700, 700))
                    thx_for_game_surface.fill((255, 255, 255))
                    thx_for_game_font = pygame.font.Font(None, 64)
                    thx_for_game_text = thx_for_game_font.render(f"Спасибо за игру!", True, pygame.color.Color('black'))
                    thx_for_game_text_x = 160
                    thx_for_game_text_y = 250
                    thx_for_game_surface.blit(thx_for_game_text, (thx_for_game_text_x, thx_for_game_text_y))
                    screen.blit(thx_for_game_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    sys.exit()
        start_end_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def end_screen():
    screen.fill((255, 255, 255))
    start_end_group.empty()
    end_sprite = pygame.sprite.Sprite(start_end_group)
    if won:
        end_sprite.image = load_image('win.png')
        pygame.mixer.music.pause()
        pygame.mixer.Sound("data/winSound.wav").play()
    else:
        end_sprite.image = load_image('lose.png')
        pygame.mixer.music.pause()
        pygame.mixer.Sound('data/loseSound.wav').play()
    end_sprite.rect = end_sprite.image.get_rect()
    end_sprite.rect.x, end_sprite.rect.y = 0, 0
    while True:
        for event_end in pygame.event.get():
            if event_end.type == pygame.QUIT:
                terminate()
            elif event_end.type == pygame.KEYDOWN or event_end.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.unpause()
                if not won:
                    score[0] = 0
                return
        start_end_group.draw(screen)
        if not won:
            final_score_surface = pygame.Surface((700, 128))
            final_score_surface.fill((255, 255, 255))
            final_score_font = pygame.font.Font(None, 64)
            final_score_text = final_score_font.render(f"Вы набрали {score[0]} очков", True,
                                                       pygame.color.Color('black'))
            final_score_text_x = 15
            final_score_text_y = 0
            final_score_surface.blit(final_score_text, (final_score_text_x, final_score_text_y))
            screen.blit(final_score_surface, (0, 500))
        pygame.display.flip()
        clock.tick(fps)


fps = 60
score = [0]
pygame.init()
pygame.display.set_caption("Йопики у ворот")
screen = pygame.display.set_mode((704, 700))
clock = pygame.time.Clock()
kf = monsters_num = start_money = health = player_x = player_y = monster_x = monster_y = monster_speed = nx = ny =\
    spawn_par = lvl = lvl_back = 0
won = False
pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
current_music = ['normal']
levels = {'first': [1, 10, 20, 4, 6, 6, 0, 0, 1, 1, 0, 1.5, 'lvl1.txt', 'lvl_back.txt'],
          'second': [1.5, 15, 30, 4, 6, 1, 2, 7, 1.7, 0, -1, 1.2, 'lvl2.txt', 'lvl_back.txt'],
          'third': [2, 20, 40, 4, 5, 5, 7, 3, 2.2, -1, 0, 1, 'lvl3.txt', 'lvl_back.txt'],
          'fourth': [5, 50, 50, 6, 5, 5, 0, 0, 5, 1, 0, 1, 'lvl4.txt', 'lvl_scary_back.txt']}
start_end_group = pygame.sprite.Group()
while True:
    won = False
    start_lvl = start_screen()
    screen = pygame.display.set_mode((704, 576))
    kf, monsters_num, money, health, player_x, player_y, monster_x, monster_y, monster_v, nx, ny, spawn_par,\
        level_text, level_back_text = start_lvl
    n = 8
    counter = 0
    end_counter = 0
    cell_width = 64
    left_top = 0

    no_sprite = pygame.sprite.Sprite()
    no_sprite.image = load_image('no_image.png')
    board_moving = Board()
    board_state = Board()
    board_player = Board()
    board_background = Board()
    board_moving.set_view(left_top, left_top, cell_width)
    board_state.set_view(left_top, left_top, cell_width)
    board_player.set_view(left_top, left_top, cell_width)
    board_background.set_view(left_top, left_top, cell_width)
    back_sprites = pygame.sprite.Group()
    moving_sprites = pygame.sprite.Group()
    state_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()

    board_background.fill(load_level(level_back_text))
    lvl = load_level(level_text)
    board_state.fill(lvl)

    hp_image = load_image("hp.png")
    money_image = load_image("coin.png")
    score_image = pygame.transform.scale(load_image("xp.png", -1), (64, 64))  # Поменять
    buttons_image = pygame.transform.scale(load_image("buttons.png"), (cell_width * 3, cell_width * 2))
    image_1 = pygame.transform.scale(load_image("1.png"), (64, 64))
    image_2 = pygame.transform.scale(load_image("2.png"), (64, 64))

    monsters = []
    towers = []
    par_monsters = monster_v * cell_width / fps
    # player = Player(player_x, player_y)
    hero_right = True
    running = True
    start = False
    screen.fill((45, 160, 95))

    hp_surface = pygame.Surface((n * cell_width // 3, cell_width))
    hp_surface.fill((45, 160, 95))
    hp_surface.blit(hp_image, (0, 0))
    hp_font = pygame.font.Font(None, 64)
    hp_text = hp_font.render(f"{health}", True, pygame.color.Color('red'))
    hp_text_x = 64
    hp_text_y = cell_width // 2 - hp_text.get_height() // 2
    hp_surface.blit(hp_text, (hp_text_x, hp_text_y))
    screen.blit(hp_surface, (0, n * cell_width))

    money_surface = pygame.Surface((n * cell_width // 3, cell_width))
    money_surface.fill((45, 160, 95))
    money_surface.blit(money_image, (0, 0))
    money_font = pygame.font.Font(None, 64)
    money_text = money_font.render(f"{money}", True, pygame.color.Color('yellow'))
    money_text_x = 64
    money_text_y = cell_width // 2 - money_text.get_height() // 2
    money_surface.blit(money_text, (money_text_x, money_text_y))
    screen.blit(money_surface, (n * cell_width // 3, n * cell_width))

    score_surface = pygame.Surface((n * cell_width // 3, cell_width))
    score_surface.fill((45, 160, 95))
    score_surface.blit(score_image, (0, 0))
    score_font = pygame.font.Font(None, 64)
    score_text = score_font.render(f"{score}", True, pygame.color.Color('green'))
    score_text_x = 64
    score_text_y = cell_width // 2 - score_text.get_height() // 2
    score_surface.blit(score_text, (score_text_x, score_text_y))
    screen.blit(score_surface, (n * cell_width // 3 * 2, n * cell_width))

    navigation_surface = pygame.Surface((cell_width * 3, cell_width * 2.5))
    navigation_surface.fill((45, 160, 95))
    navigation_surface.blit(buttons_image, (0, cell_width * 0.5))
    navigation_font = pygame.font.Font(None, 45)
    navigation_text = navigation_font.render("Управление", True, pygame.color.Color('white'))
    navigation_text_x = 0
    navigation_text_y = 0
    navigation_surface.blit(navigation_text, (navigation_text_x, navigation_text_y))
    screen.blit(navigation_surface, (n * cell_width, 0))

    surface_1 = pygame.Surface((cell_width * 3, cell_width * 2))
    surface_1.fill((45, 160, 95))
    surface_1.blit(image_1, (0, cell_width * 1))
    surface_1_font = pygame.font.Font(None, 64)
    surface_1_text = surface_1_font.render("Маг", True, pygame.color.Color('white'))
    surface_1_text_x = 0
    surface_1_text_y = 0
    surface_1.blit(surface_1_text, (surface_1_text_x, surface_1_text_y))
    surface_1_text_2 = surface_1_font.render("(земля)", True, pygame.color.Color('white'))
    surface_1_text_2_x = 0
    surface_1_text_2_y = cell_width * 0.5
    surface_1.blit(surface_1_text_2, (surface_1_text_2_x, surface_1_text_2_y))
    screen.blit(surface_1, (n * cell_width, cell_width * 2.5))

    surface_2 = pygame.Surface((cell_width * 3, cell_width * 2))
    surface_2.fill((45, 160, 95))
    surface_2.blit(image_2, (0, cell_width * 1))
    surface_2_font = pygame.font.Font(None, 64)
    surface_2_text = surface_2_font.render("Лучник", True, pygame.color.Color('white'))
    surface_2_text_x = 0
    surface_2_text_y = 0
    surface_2.blit(surface_2_text, (surface_2_text_x, surface_2_text_y))
    surface_2_text_2 = surface_2_font.render("(воздух)", True, pygame.color.Color('white'))
    surface_2_text_2_x = 0
    surface_2_text_2_y = cell_width * 0.5
    surface_2.blit(surface_2_text_2, (surface_2_text_2_x, surface_2_text_2_y))
    screen.blit(surface_2, (n * cell_width, cell_width * 4.5))

    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        board_background.render(back_sprites, screen)
        board_state.render(state_sprites, screen)
        board_moving.render(moving_sprites, screen)
        board_player.render(hero_sprite, screen)

        hp_surface.fill((45, 160, 95))
        hp_surface.blit(hp_image, (0, 0))
        hp_text = hp_font.render(f"{health}", True, pygame.color.Color('red'))
        hp_text_x = 64
        hp_text_y = cell_width // 2 - hp_text.get_height() // 2
        hp_surface.blit(hp_text, (hp_text_x, hp_text_y))
        screen.blit(hp_surface, (0, n * cell_width))

        money_surface.fill((45, 160, 95))
        money_surface.blit(money_image, (0, 0))
        money_text = money_font.render(f"{money}", True, pygame.color.Color('yellow'))
        money_text_x = 64
        money_text_y = cell_width // 2 - money_text.get_height() // 2
        money_surface.blit(money_text, (money_text_x, money_text_y))
        screen.blit(money_surface, (n * cell_width // 3, n * cell_width))

        score_surface.fill((45, 160, 95))
        score_surface.blit(score_image, (0, 0))
        score_text = score_font.render(f"{score[0]}", True, pygame.color.Color('green'))
        score_text_x = 64
        score_text_y = cell_width // 2 - score_text.get_height() // 2
        score_surface.blit(score_text, (score_text_x, score_text_y))
        screen.blit(score_surface, (n * cell_width // 3 * 2, n * cell_width))

        clock.tick(fps)
        pygame.display.flip()
        counter += 1
        if end_counter >= 120:
            won = True
            break
    end_screen()
