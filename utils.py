import const as C
import classes.entities as e

TILES = []


# Парсинг файла карты
def create_tiles_from_file(path: str):
    pass


# Получение типа клетки по ее символьному коду
def get_tile_type(code: str):
    return C.tile_types[code]


# Создание карты по массиву с инструкциями
def create_tiles(tiles):
    x = 0
    while x < C.TILES_X:
        y = 0
        while y < C.TILES_Y:
            tile_type = get_tile_type(tiles[x][y])
            TILES.append(e.Tile())
            y += 1
        x += 1
