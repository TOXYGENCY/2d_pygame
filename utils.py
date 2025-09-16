from typing import List
import const as C
import entities as e
import pygame as pg

TILES: List[e.Tile] = []


# Создание карты по массиву с инструкциями
def create_tiles(tiles):
    y = 0
    while y <= len(tiles) - 1:
        x = 0
        tile_row = []
        while x <= len(tiles[y]) - 2:  # скипаем последний \n
            tile_row.append(e.Tile(tiles[y][x]))
            x += 1
        TILES.append(tile_row)
        y += 1


# Парсинг файла карты
def create_tiles_from_file(path: str):
    file = open(path, "r")
    lines = file.readlines()
    create_tiles(lines)
    # print(TILES)


# функция отрисовки клеток
def render_tiles(screen: pg.Surface):
    y = 0
    while y <= len(TILES) - 1:
        x = 0
        while x <= len(TILES[y]) - 1:
            screen.blit(
                TILES[y][x].sprite, (C.SPRITE_SIZE * x, C.SPRITE_SIZE * y)
            )
            if TILES[y][x].entity:
                screen.blit(
                    TILES[y][x].entity.sprite,
                    ((C.SPRITE_SIZE * x), (C.SPRITE_SIZE * y)),
                )
            x += 1
        y += 1
