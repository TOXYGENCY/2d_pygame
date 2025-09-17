from typing import List
import const as C
import pygame as pg


# Общий класс для всех элементов со спрайтами
class Sprited:
    def __init__(self, sprite_path: str):
        self.sprite_path = sprite_path

        # Загрузка спрайта
        self.sprite = pg.image.load(sprite_path).convert_alpha()


# Клетка
class Tile(Sprited):

    def __init__(self, type_code: str):

        self.assign_sprite(type_code)
        super().__init__(self.sprite_path)
        self.type_code = type_code
        self.entity = None
        self.assign_entity()
        self.occupied = False
        self.refresh_occupation()

    # Автоназначение спрайта по символьному коду её типа
    def assign_sprite(self, type_code):
        self.sprite_path = C.tile_types[type_code]

    # Автоназначение сущности
    def assign_entity(self):
        type = self.type_code
        ent = None
        if type == "P":
            ent = Player(self)
        elif type == "X":
            ent = Enemy(self)
        elif type == "C":
            ent = Collectable(self)
        elif type == "2":
            ent = Prop(self)
        elif type == "N":
            ent = NPC(self)
        self.entity = ent

    # проверка занятости
    def refresh_occupation(self):
        if self.entity:
            self.occupied = True
        else:
            self.occupied = False


# Сущность
class Entity(Sprited):

    def __init__(self, type: str, tile: Tile):
        # self.assign_sprite(role)
        super().__init__(type)
        self.tile = tile
        self.type = type

    # Автоназначение спрайта по символьному коду её типа
    # def assign_sprite(self, entity_code):
    #     self.sprite_path = C.entity_types[entity_code]


# Декор
class Prop(Entity):

    def __init__(self, tile: Tile):
        super().__init__(C.entity_types["2"], tile)


# коллектабл
class Collectable(Entity):

    def __init__(self, tile: Tile):
        super().__init__(C.entity_types["C"], tile)
        self.collected = False


# npc (движущийся декор)
class NPC(Entity):

    def __init__(self, tile: Tile):
        super().__init__(C.entity_types["N"], tile)


# враг (npc который преследует игрока)
class Enemy(Entity):

    def __init__(self, tile: Tile):
        super().__init__(C.entity_types["X"], tile)


# Сущность игрока
class Player(Entity):

    def __init__(self, tile: Tile):
        super().__init__(C.entity_types["P"], tile)

    def move(self, direction):
        self


class Level:
    def __init__(self, level_path: str):
        # Список со всеми рядами клеток
        self.tiles: List[List[Tile]] = [[]]
        self.level_path = level_path
        self.tiles = self.create_tiles_from_file(level_path)

    # Создание карты по массиву с инструкциями
    def create_tiles(self, tiles) -> List[List[Tile]]:
        level_tiles = []
        y = 0
        while y <= len(tiles) - 1:
            x = 0
            tile_row = []
            while x <= len(tiles[y]) - 1:
                tile_row.append(Tile(tiles[y][x]))
                x += 1
            level_tiles.append(tile_row)
            y += 1
        return level_tiles

    # Парсинг файла карты
    def create_tiles_from_file(self, path: str) -> List[List[Tile]]:
        file = open(path, "r")
        lines = file.read()  # читаем все как есть
        lines = lines.split("\n")  # делим и убираем переносы
        return self.create_tiles(lines)

    # функция отрисовки клеток
    def render_tiles(self, screen: pg.Surface):
        y = 0
        while y <= len(self.tiles) - 1:
            x = 0
            while x <= len(self.tiles[y]) - 1:
                # отрисовка клетки
                screen.blit(
                    self.tiles[y][x].sprite,
                    (C.SPRITE_SIZE * x, C.SPRITE_SIZE * y),
                )
                # отрисовка самой сущности, если она есть
                if self.tiles[y][x].entity:
                    screen.blit(
                        self.tiles[y][x].entity.sprite,
                        ((C.SPRITE_SIZE * x), (C.SPRITE_SIZE * y)),
                    )
                x += 1
            y += 1
