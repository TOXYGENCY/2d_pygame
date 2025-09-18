from typing import List
import const as C
import pygame as pg

all_entities = []


# Общий класс для всех элементов со спрайтами
class Sprited:
    def __init__(self, sprite_path: str):
        self.sprite_path = sprite_path

        # Загрузка спрайта
        self.sprite = pg.image.load(sprite_path).convert_alpha()


# Клетка
class Tile(Sprited):

    def __init__(self, type_code: str, x: int, y: int):
        self.assign_sprite(type_code)
        super().__init__(self.sprite_path)
        self.x = x
        self.y = y
        self.type_code = type_code
        self.entity = None
        self.assign_entity()
        self.occupied = False
        self.refresh_occupation()

    # Автоназначение спрайта по символьному коду её типа
    def assign_sprite(self, type_code):
        self.sprite_path = C.tile_types[type_code]

    # очистка сущности
    def clear_entity(self):
        self.entity = None

    # Автоназначение сущности
    def assign_entity(self, entity=None):
        type = self.type_code

        if not entity:
            if type == "P":
                entity = Player(self)
            elif type == "X":
                entity = Enemy(self)
            elif type == "C":
                entity = Collectable(self)
            elif type == "2":
                entity = Prop(self)
            elif type == "N":
                entity = NPC(self)

        if entity:
            all_entities.append(entity)

        self.entity = entity

    # проверка занятости
    def refresh_occupation(self):
        if self.entity:
            self.occupied = True
        else:
            self.occupied = False


# Сущность
class Entity(Sprited):

    def __init__(self, type: str, tile: Tile):
        super().__init__(type)
        self.tile = tile
        self.type = type


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


# Класс содержащий всю информацию об уровне
class Level:
    def __init__(self, level_path: str):
        # Список со всеми рядами клеток
        self.tiles = self.create_tiles_from_file(level_path)
        self.level_path = level_path
        self.player = list(
            filter(lambda x: isinstance(x, Player), all_entities)
        )[0]
        self.player_xy = (self.player.tile.x, self.player.tile.y)

    # Создание карты по массиву с инструкциями
    def create_tiles(self, tiles) -> List[List[Tile]]:
        level_tiles = []
        y = 0
        while y <= len(tiles) - 1:
            x = 0
            tile_row = []
            while x <= len(tiles[y]) - 1:
                tile_row.append(Tile(tiles[y][x], x, y))
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

    # перемещение игрока. direction: (x, y) но с перевернутым y
    def move_player(self, direction: tuple[int, int]):
        # player_xy: (x, y)
        new_player_xy = (
            self.player_xy[0] + direction[0],  # складываем x
            self.player_xy[1] + direction[1] * -1,  # складываем y
        )

        this_tile = self.get_tile(self.player_xy[0], self.player_xy[1])
        next_tile = self.get_tile(new_player_xy[0], new_player_xy[1])

        if next_tile:
            # Если уже есть сущность
            if next_tile.occupied:
                if isinstance(next_tile.entity, Enemy):
                    self.game_over("Enemy got you!")
                elif isinstance(next_tile.entity, NPC) or isinstance(
                    next_tile.entity, Prop
                ):
                    self.game_over("You crashed.")
                elif isinstance(next_tile.entity, Collectable):
                    self.collect_collectable("+1000 у.е.")
            # Если выход
            elif next_tile.type_code == "E":
                self.level_passed()

        this_tile.clear_entity()
        next_tile.assign_entity(self.player)
        self.player_xy = new_player_xy

    # поиск конкретной клетки по координатам
    def get_tile(self, x, y) -> Tile | None:
        if y >= len(self.tiles):
            print(
                f"""Index error upon searching for tile.
                Y coordinate is out of bounds ({y} >= {len(self.tiles)})."""
            )
            return None
        elif x >= len(self.tiles[y]):
            print(
                f"""Index error upon searching for tile.
                X coordinate is out of bounds ({x} >= {len(self.tiles[y])})."""
            )
            return None
        else:
            return self.tiles[y][x]

    def collect_collectable(self, mes="You picked up a collectable"):
        print(mes)

    def level_passed(self):
        print("Congratulations, You Win!")

    def game_over(self, message):
        print(f"GAME OVER. {message}")

    def debug(self):
        print(all_entities)
