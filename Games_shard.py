import pygame
import sys
import pymorphy2
import random
import time
import os
morph = pymorphy2.MorphAnalyzer()
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_image(name):
    # загрузка изображения и его обработка
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


camera = Camera()
# изображения спрайтов
tile_images = {'wall': [load_image('wall.png'), load_image('wall1.png')],
               'empty': [load_image('grass.png'), load_image('grass2.png')],
               'portal': [load_image('portal.png')]}
# переменная, отвечающая за кол-во собранных ключей
keys = 0
# изображения анимаций
player_image = load_image('hero_down1.png')
animation_right = [load_image('hero_right1.png'), load_image('hero_right2.png'),
                   load_image('hero_right1.png'), load_image('hero_right3.png')]
animation_left = [load_image('hero_left1.png'), load_image('hero_left2.png'),
                  load_image('hero_left1.png'), load_image('hero_left3.png')]
animation_up = [load_image('hero_up1.png'), load_image('hero_up2.png'),
                load_image('hero_up1.png'), load_image('hero_up3.png')]
animation_down = [load_image('hero_down1.png'), load_image('hero_down2.png'),
                  load_image('hero_down1.png'), load_image('hero_down3.png')]
# размер клетки
tile_width = tile_height = 80
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
keys_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


def generate_level(level):
    # маршруты движения врагов
    paths = [['x+', 'x+', 'y-', 'y-', 'x-', 'x-', 'y+', 'y+'],
             ['x+', 'y-',  'y-', 'y-', 'y-', 'y+', 'y+', 'y+',
              'y+', 'x-'],
             ['y-', 'y-', 'y-', 'y-', 'y+', 'y+', 'y+', 'y+'],
             ['x+', 'x+', 'y-', 'x+', 'x+', 'y+', 'x+', 'x+',
              'x+', 'x-', 'x-', 'x-', 'y-', 'x-', 'x-', 'y+',
              'x-', 'x-']]
    # размещение объектов согласно текстовой карте
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Enemy(x, y, paths[0])
                del paths[0]
            elif level[y][x] == 'K':
                Tile('empty', x, y)
                Key(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                Tile('portal', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = random.choice(tile_images[tile_type])
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        # определение и создание спрайта клетки

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
        # определение и создание игрока

    def update(self):
        global keys
        if keys == 4 and level_map[self.y][self.x] == '*':
            return False
        return True
    # проверка условия выигрыша

    def move_right(self):
        self.x += 1
        self.rect.x += tile_width
        self.image = load_image('None.png')
        self.image = animation_right[0]
        animation_right.append(animation_right[0])
        del animation_right[0]
        # движение вправо с анимацией

    def move_left(self):
        self.x -= 1
        self.rect.x -= tile_width
        self.image = load_image('None.png')
        self.image = animation_left[0]
        animation_left.append(animation_left[0])
        del animation_left[0]
        # движение влево с анимацией

    def move_up(self):
        self.y -= 1
        self.rect.y -= tile_height
        self.image = load_image('None.png')
        self.image = animation_up[0]
        animation_up.append(animation_up[0])
        del animation_up[0]
        # движение вверх с анимацией

    def move_down(self):
        self.y += 1
        self.rect.y += tile_height
        self.image = load_image('None.png')
        self.image = animation_down[0]
        animation_down.append(animation_down[0])
        del animation_down[0]
        # движение вниз с анимацией


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, path):
        super().__init__(enemies_group, all_sprites)
        self.image = random.choice((load_image('enemy2.png'), load_image('enemy3.png'),
                                    load_image('enemy1.png'), load_image('enemy4.png')))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
        # определение и создание спрайта врага
        self.path = []
        for direction in path:
            for _ in range(10):
                self.path.append(direction)
        # считывание и запись маршрута

    def update(self):
        if self.path[0] == 'y+':
            self.rect.y += tile_height * 0.1
            self.y += 0.1
        elif self.path[0] == 'y-':
            self.rect.y -= tile_height * 0.1
            self.y -= 0.1
        elif self.path[0] == 'x-':
            self.rect.x -= tile_width * 0.1
            self.x -= 0.1
        elif self.path[0] == 'x+':
            self.rect.x += tile_height * 0.1
            self.x += 0.1
        self.path.append(self.path[0])
        del self.path[0]
        if player.x == round(self.x) and player.y == round(self.y):
            player.rect.x, player.rect.y = player.rect.x - (player.x - 2) * tile_width,\
                                           player.rect.y - (player.y - 1) * tile_height
            player.x, player.y = 2, 1
            player.image = load_image('hero_down1.png')
        # движение врага по заданному маршруту и проверка условия контакта с игроком


class Key(pygame.sprite.Sprite):
    key_image = load_image('key.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(keys_group, all_sprites)
        self.image = self.key_image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y + 30)
        self.x = pos_x
        self.y = pos_y
        self.exist = True
        # определение и создание спрайта ключа

    def update(self):
        global keys
        if self.x == player.x and self.y == player.y and self.exist is True:
            self.exist = False
            self.image = load_image('None.png')
            keys += 1
        # проверка условия контакта с игроком


def terminate():
    pygame.quit()
    sys.exit()
    # выход из программы


def start_screen(intro_text, picture='fon.jpg'):
    # вызов окна с фоном и текстом, которые задаются при вызове функции
    fon = pygame.transform.scale(load_image(picture), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 29)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, (34, 255, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(50)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        map_level = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, map_level))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), map_level))


level_map = load_level("map.txt")
player, level_x, level_y = generate_level(level_map)
running = True
start_screen(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '',  '          Осколок мира игр',
              'Мир игр столкнулся с этим миром.', 'Пройдите все игры оставшегося осколка и уничтожьте его!'], 'start.png')
start_screen(['', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Лабиринт и знаки', '',
                  'Не касайтесь знаков, соберите все ключи и найдите портал!',
                  'Управление персонажем осуществляется WASD или стрелками клавиатуры'])

while running:
    # основной цикл первого уровня
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif not player.update():
            running = False
        if event.type != pygame.KEYDOWN:
            continue
        button = pygame.key.get_pressed()
        if sum(button) > 1:
            continue
        # перемещения игрока
        elif button[pygame.K_DOWN] or button[pygame.K_s]:
            if level_map[player.y + 1][player.x] != '#':
                player.move_down()
        elif button[pygame.K_UP] or button[pygame.K_w]:
            if level_map[player.y - 1][player.x] != '#':
                player.move_up()
        elif button[pygame.K_RIGHT] or button[pygame.K_d]:
            if level_map[player.y][player.x + 1] != '#':
                player.move_right()
        elif button[pygame.K_LEFT] or button[pygame.K_a]:
            if level_map[player.y][player.x - 1] != '#':
                player.move_left()
    screen.fill((0, 255, 255))
    all_sprites.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)
    # изменяем ракурс камеры
    camera.update(player)
    for el in all_sprites:
        el.update()
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    pygame.display.flip()
    clock.tick(60)

# второй уровень задан функцией, так как существует условие проигрыша


def level_2():
    start_screen(['', '', '', '', '', '', '', '', '', '', '', '', 'Игра обманов', '',
                  'Ход должен быть сделан так, чтобы непрерывный ряд фишек соперника', 'оказался «закрыт»'
                  ' фишками игрока с двух сторон. Выигрывает тот,', 'у кого к концу игры больше фишек.',
                                                                    'Желтыми полями подсвечены возможные ходы.'])

    class Board:
        # создание поля
        def __init__(self, w, h):
            self.width = w
            self.height = h
            self.board = [[' '] * w for _ in range(h)]
            self.cell_size = 100

        def render(self):
            # отображение поля на экране
            for y in range(self.height):
                for x in range(self.width):
                    color = pygame.Color('black')
                    if self.board[y][x] == "X":
                        pygame.draw.circle(screen, (41, 49, 51), (x * self.cell_size + self.cell_size // 2 + 1,
                                                                  y * self.cell_size + self.cell_size // 2 + 1),
                                           self.cell_size // 2 - 2, 0)
                    elif self.board[y][x] == 'O':
                        pygame.draw.circle(screen, (214, 206, 204), (x * self.cell_size + self.cell_size // 2 + 1,
                                                                     y * self.cell_size + self.cell_size // 2 + 1),
                                           self.cell_size // 2 - 2, 0)
                    elif self.board[y][x] == '!' and not game.computer_turn:
                        color = pygame.Color('yellow')
                    pygame.draw.rect(screen, color,
                                     (x * self.cell_size + 2,
                                      y * self.cell_size + 2,
                                      self.cell_size - 2, self.cell_size - 2), 1)
            pygame.draw.rect(screen, (6, 139, 54), (0, 0, 801, 801), 5)

        def get_cell(self, xy):
            # возвращает координату клетки в матрице клеток
            x, y = xy[0], xy[1]
            cell_x = x // self.cell_size
            cell_y = y // self.cell_size
            return cell_x, cell_y

    class Othello(Board):
        def __init__(self, w, h):
            super().__init__(w, h)
            # инициализация Отелло
            self.width, self.height = w, h
            tiles = ['X', 'O']
            random.shuffle(tiles)
            self.player_tile, self.computer_tile = tiles
            self.showHints = False
            self.computer_turn = self.computer_tile is "X"
            self.board[3][4] = "O"
            self.board[3][3] = "X"
            self.board[4][4] = "X"
            self.board[4][3] = "O"

        @staticmethod
        def on_board(x, y):
            # проверка нахождения на поле "клика"
            return 0 <= x <= 7 and 0 <= y <= 7

        @staticmethod
        def on_corner(x, y):
            # в углу ли клетка
            return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

        def valid_move(self, tile, xstart, ystart):
            # возвращает возможность хода и перевернутые фишки после этого хода
            if not self.on_board(xstart, ystart):
                return False
            if self.board[xstart][ystart] not in [' ', '!']:
                return False
            self.board[xstart][ystart] = tile
            if tile == 'X':
                other_tile = 'O'
            else:
                other_tile = 'X'
            flip_tiles = []
            for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                x, y = xstart, ystart
                x += xdirection
                y += ydirection
                if self.on_board(x, y) and self.board[x][y] == other_tile:
                    x += xdirection
                    y += ydirection
                    if not self.on_board(x, y):
                        continue
                    while self.board[x][y] == other_tile:
                        x += xdirection
                        y += ydirection
                        if not self.on_board(x, y):
                            break
                    if not self.on_board(x, y):
                        continue
                    if self.board[x][y] == tile:
                        while True:
                            x -= xdirection
                            y -= ydirection
                            if x == xstart and y == ystart:
                                break
                            flip_tiles.append([x, y])
            self.board[xstart][ystart] = ' '
            if len(flip_tiles) == 0:
                return False
            return flip_tiles

        def hints_board(self):
            # возвращает поле с возможными ходами
            hints_board = self.board.copy()
            for x, y in self.get_valid_moves(self.player_tile):
                hints_board[x][y] = '!'
            return hints_board

        def get_valid_moves(self, tile):
            # возвращает возможные ходы
            valid_moves = []
            for x in range(8):
                for y in range(8):
                    if self.valid_move(tile, x, y):
                        valid_moves.append([x, y])
            return valid_moves

        def play_again(self):
            global game
            # начать игру заново, в случае ничьи или проигрыша игрока
            game = Othello(self.width, self.height)

        def board_score(self, board):
            # возвращает кол-во фишек компьютера и игрока
            score_list = self.linear(board)
            return score_list.count(self.computer_tile), score_list.count(self.player_tile)

        def linear(self, some_list):
            # превращает список списков в строку
            if type(some_list) != list:
                return [some_list]
            if not some_list:
                return []
            else:
                return self.linear(some_list[:-1]) + self.linear(some_list[-1])

        def plan_move(self, plan_board, tile, xstart, ystart):
            # возвращает состояние доски после предполагаемого хода
            tiles_to_flip = self.valid_move(tile, xstart, ystart)
            if not tiles_to_flip:
                return False
            plan_board[xstart][ystart] = tile
            for x, y in tiles_to_flip:
                plan_board[x][y] = tile
            return plan_board

        def computer_move(self):
            # анализирует наилучший ход для компьютера и осуществляет его
            best_move = False
            possible_moves = self.get_valid_moves(self.computer_tile)
            random.shuffle(possible_moves)
            for x, y in possible_moves:
                if self.on_corner(x, y):
                    self.computer_turn = False
                    self.board = self.plan_move(self.board, self.computer_tile, x, y)
                    return True
            best_score = -1
            for x, y in possible_moves:
                plan_board = self.copy_board()
                self.plan_move(plan_board, self.computer_tile, x, y)
                score = self.board_score(plan_board)[0]
                # выбираем ход с наибольшим кол-вом переворачиваемых фишек
                if score > best_score:
                    best_move = [x, y]
                    best_score = score
            self.computer_turn = False
            if 0 in self.board_score(game.board) or self.linear(self.board).count(' ') +\
                    self.linear(self.board).count('!') == 0:
                return False
            if best_move is False:
                return True
            self.board = self.plan_move(self.board, self.computer_tile, best_move[0], best_move[1])
            return True

        def copy_board(self):
            # возвращает копию доски
            some_list = []
            for i in self.board:
                other_list = []
                for j in i:
                    other_list.append(j)
                some_list.append(other_list)
            return some_list

        def on_click(self, cell):
            # проверяет возможность хода игрока и осуществляет его
            if self.plan_move(self.copy_board(), self.player_tile, cell[1], cell[0]) is False:
                return
            self.board = self.plan_move(self.copy_board(), self.player_tile, cell[1], cell[0])
            self.render()
            self.computer_turn = True

        def get_click(self, mouse_pos):
            # получает координату клетки, на которую кликнули, и реализует ход
            cell = self.get_cell(mouse_pos)
            self.on_click(cell)

    # в Отелло играют на поле 8 * 8 поэтому требуется поле кратное 800 по высоте и ширине.
    new_size = 801, 801
    new_screen = pygame.display.set_mode(new_size)
    game = Othello(8, 8)
    if game.computer_turn:
        time.sleep(0.5)
        game.computer_move()
    working = True
    while working:
        # основной цикл второго уровня
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if not game.computer_turn:
                    if 0 in game.board_score(game.board) or game.linear(game.board).count(' ')\
                            + game.linear(game.board).count('!') == 0:
                        # если у игрока и компьютера нет возможных ходов, выходим из цикла
                        working = False
                        break
                    game.get_click(e.pos)
        new_screen.fill((6, 139, 54))
        computer_board = game.copy_board()
        game.board = game.hints_board()
        if game.linear(game.board).count('!') == 0:
            game.computer_turn = True
        if game.computer_turn:
            game.board = computer_board
        game.render()
        pygame.display.flip()
        if game.computer_turn:
            time.sleep(0.5)
            working = game.computer_move()
    # экран победы это картинка 800 на 600, переделываем размер окна программы
    pygame.display.set_mode((800, 600))
    # подсчитываем фишки
    player_score = game.board_score(game.board)[1]
    computer_score = game.board_score(game.board)[0]
    comment = morph.parse('очко')[0]
    # выводим на экран кто и на сколько фишек победил
    if computer_score > player_score:
        start_screen(['                                                    Победа компьютера на '
                      + str(computer_score - player_score) + ' '
                      + comment.make_agree_with_number(computer_score - player_score).word], 'end.jpg')
        level_2()
    elif computer_score < player_score:
        start_screen(['                                                    Победа игрока на '
                      + str(player_score - computer_score) + ' '
                      + comment.make_agree_with_number(player_score - computer_score).word], 'end.jpg')
    else:
        start_screen(['                                                                      Ничья'], 'end.jpg')
        level_2()
    start_screen([''], 'end_game.jpg')
    # игра кончается тогда и только тогда, когда игрок выигрывает
    terminate()


level_2()
