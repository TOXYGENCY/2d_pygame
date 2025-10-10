import random
from typing import List

import vars as v
import pygame as pg

all_entities = []


def get_from_sprite_set(sprite_set, key):
    return pg.image.load(sprite_set[key]).convert_alpha()


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
        self.sprite_rotation = random.randint(1, 4)
        self.type_code = type_code
        self.entity = None
        self.assign_entity()
        self.occupied = False
        self.refresh_occupation()

    # Автоназначение спрайта по символьному коду её типа
    def assign_sprite(self, type_code):
        self.sprite_path = v.tile_types[type_code]

    # очистка сущности
    def clear_entity(self):
        self.entity = None
        self.refresh_occupation()

    # Автоназначение сущности
    def assign_entity(self, entity=None):
        type = self.type_code

        if not entity:
            if type == "P":
                entity = Player(self)
                all_entities.append(entity)
            elif type == "X":
                entity = Enemy(self)
                all_entities.append(entity)
            elif type == "C":
                entity = Collectable(self)
                all_entities.append(entity)
            elif type == "2":
                entity = Prop(self)
                all_entities.append(entity)
            elif type == "N":
                entity = NPC(self)
                all_entities.append(entity)

        self.entity = entity
        self.refresh_occupation()

    # проверка занятости
    def refresh_occupation(self):
        if self.entity or self.type_code in "12":
            self.occupied = True
        else:
            self.occupied = False


# Сущность
class Entity(Sprited):

    def __init__(self, type_code: str, tile: Tile):
        self.type_code = type_code
        sprite_path = v.entity_types[type_code]
        super().__init__(sprite_path)
        self.tile = tile
        self.sprite_set = None
        self.next_tile = None
        self.next_direction = (0, 0)

    # Изменение спрайта для сущности
    def change_sprite(self, key: str):
        if self.sprite_set:
            self.sprite = get_from_sprite_set(self.sprite_set, key)
        else:
            print("Requested change for an entity with no sprite set")

    # Назначение следующей клетки
    def set_new_tile(self, next_tile):
        self.next_tile = next_tile
        self.set_next_direction_sprite()

    # Изменение спрайта сущности в зависимости от СЛЕДУЮЩЕГО направления
    def set_next_direction_sprite(self, next_direction):
        self.next_direction = next_direction
        if next_direction == (0, -1):
            self.change_sprite("UP")
        elif next_direction == (0, 1):
            self.change_sprite("DOWN")
        elif next_direction == (1, 0):
            self.change_sprite("RIGHT")
        elif next_direction == (-1, 0):
            self.change_sprite("LEFT")


# Декор
class Prop(Entity):

    def __init__(self, tile: Tile):
        super().__init__("2", tile)


# коллектабл
class Collectable(Entity):

    def __init__(self, tile: Tile):
        super().__init__("C", tile)
        self.collected = False


# npc (движущийся декор)
class NPC(Entity):

    def __init__(self, tile: Tile):
        super().__init__("N", tile)
        self.sprite_set = v.npc_sprites


# враг (npc который преследует игрока)
class Enemy(Entity):

    def __init__(self, tile: Tile):
        super().__init__("X", tile)
        self.sprite_set = v.enemy_sprites


# Сущность игрока
class Player(Entity):

    def __init__(self, tile: Tile):
        super().__init__("P", tile)
        self.sprite_set = v.player_sprites


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
        self.moves_score = 0

    # Проверка смерти игрока (используется после передвижения врага)
    def check_player_death(self):
        if (
            self.player.tile.entity is not None
            and self.player.tile.entity.type_code != "P"
        ):
            self.game_over("Enemy got you!")

    # Передвижение всех сущностей
    def move_all_entities(self):
        i = 0
        while i < len(all_entities):
            if all_entities[i].type_code in "XN":
                self.move_entity(all_entities[i])
                self.check_player_death()
            i += 1

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
                # если это стена - то случайно поворачиваем спрайт
                if self.tiles[y][x].type_code == "1":
                    screen.blit(
                        pg.transform.rotate(
                            self.tiles[y][x].sprite,
                            self.tiles[y][x].sprite_rotation * 90,
                        ),
                        (v.SPRITE_SIZE * x, v.SPRITE_SIZE * y),
                    )
                else:
                    # иначе просто отрисовываем
                    screen.blit(
                        self.tiles[y][x].sprite,
                        (v.SPRITE_SIZE * x, v.SPRITE_SIZE * y),
                    )
                # отрисовка самой сущности, если она есть
                if self.tiles[y][x].entity:
                    screen.blit(
                        self.tiles[y][x].entity.sprite,
                        ((v.SPRITE_SIZE * x), (v.SPRITE_SIZE * y)),
                    )
                x += 1
            y += 1

    # Проверка, доступна ли клетка для сущности
    def is_tile_available_for_entity(
        self, tile: Tile, entity_type: str = None
    ) -> bool:
        # Для сущностей-врагов
        if entity_type == "X":
            # Если на клетке есть игрок, то она доступна
            if (
                tile is not None
                and tile.entity is not None
                and tile.entity.type_code == "P"
            ):
                return True

        # Для остальных сущностей
        return tile is not None and (
            not tile.occupied and tile.type_code not in "12EC"
        )

    # Рассчитать клетки для перемещения сущности
    def calc_next_tiles(
        self,
        this_tile: Tile,
        entity: Entity,
    ):
        # список доступных направлений
        directions = list(v.DIRECTIONS.values())
        directions.remove((0, 0))
        random.shuffle(directions)

        # поиск первой доступной клетки
        next_tile = None
        i1 = 0
        while i1 < len(directions) and not (
            self.is_tile_available_for_entity(next_tile, entity.type_code)
        ):
            next_direction = directions[i1]
            next_tile = self.get_tile(
                this_tile.x + next_direction[0],
                this_tile.y + next_direction[1],
            )
            i1 += 1

        # если ни одна клетка по НАПРАВЛЕНИЮ не доступна, то ставим this_tile
        # решение принимается на основе счетчика рассмотренных направлений
        if i1 == len(directions) and not self.is_tile_available_for_entity(
            next_tile, entity.type_code
        ):
            next_tile = this_tile

        # поиск второй доступной клетки
        random.shuffle(directions)
        next_tile2 = None
        i2 = 0
        while i2 < len(directions) and not (
            self.is_tile_available_for_entity(next_tile2, entity.type_code)
        ):
            next_direction2 = directions[i2]
            next_tile2 = self.get_tile(
                next_tile.x + next_direction2[0],
                next_tile.y + next_direction2[1],
            )
            i2 += 1

        if i2 == len(directions) and not self.is_tile_available_for_entity(
            next_tile2, entity.type_code
        ):
            next_tile2 = this_tile

        # Возвращаем все, потому что в другом месте это нужнее
        return next_tile, next_tile2, next_direction, next_direction2

    # Переместить сущность. direction: (x, y)
    def move_entity(
        self,
        entity: Entity,
    ):
        # определяем текущую клетку
        this_tile = self.get_tile(entity.tile.x, entity.tile.y)

        # если уже определена след. клетка - используем
        if entity.next_tile and self.is_tile_available_for_entity(
            entity.next_tile
        ):
            next_tile = entity.next_tile
            next_tile2, _, entity.next_direction, _ = self.calc_next_tiles(
                next_tile, entity
            )
        else:
            next_tile, next_tile2, _, entity.next_direction = (
                self.calc_next_tiles(this_tile, entity)
            )

        # если обе клетки доступны, то передвигаем и меняем спрайт
        if self.is_tile_available_for_entity(
            next_tile, entity.type_code
        ) and self.is_tile_available_for_entity(next_tile2):
            this_tile.clear_entity()
            next_tile.assign_entity(entity)
            entity.tile = next_tile
            entity.next_tile = next_tile2
            entity.set_next_direction_sprite(entity.next_direction)

        # если только одна клетка доступна, то просто передвигаем
        elif self.is_tile_available_for_entity(next_tile, entity.type_code):
            this_tile.clear_entity()
            next_tile.assign_entity(entity)
            entity.tile = next_tile

    # перемещение игрока. direction: (x, y) но с перевернутым y
    def move_player(self, direction: tuple[int, int]):
        # player_xy: (x, y)
        new_player_xy = (
            self.player_xy[0] + direction[0],  # складываем x
            self.player_xy[1] + direction[1],  # складываем y
        )

        # Изменение спрайта персонажа в зависимости от направления
        if direction == (0, 1):
            self.player.change_sprite("DOWN")
        elif direction == (0, -1):
            self.player.change_sprite("UP")
        elif direction == (1, 0):
            self.player.change_sprite("RIGHT")
        elif direction == (-1, 0):
            self.player.change_sprite("LEFT")

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
                # Если стена
                elif next_tile.type_code == "1":
                    self.game_over("You crashed into a wall.")
            # Если выход
            elif next_tile.type_code == "E":
                self.level_passed()

            # Само передвижение персонажа (переназначение клеток)
            this_tile.clear_entity()
            next_tile.assign_entity(self.player)
            self.player.tile = next_tile
            self.player_xy = new_player_xy
            if direction != (0, 0):
                self.moves_score += 1
        else:
            pass

    # поиск конкретной клетки по координатам
    def get_tile(self, x, y) -> Tile | None:
        if x < 0 or y < 0:
            print(f"No tile with negative coordinates. ({x},{y})")
            return None

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

    # Сбор коллекционного предмета
    def collect_collectable(self, mes=v.COLLECTABLE_MES):
        print(mes)

    # Уровень пройден
    def level_passed(self):
        v.show_win_mes = True
        v.show_lost_mes = False
        v.should_move_entities = False
        # v.tick_rate = 3
        print(v.WIN_MES)

    # Уровень проигран
    def game_over(self, message):
        v.show_win_mes = False
        v.show_lost_mes = True
        v.should_move_entities = False
        # v.tick_rate = 3
        v.lost_mes = f"GAME OVER. {message}"
        print(v.lost_mes)

    # Дебаг, не обращать внимания
    def debug(self):
        pass
