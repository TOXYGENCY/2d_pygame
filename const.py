# from enum import Enum

# Константы игры

WINDOW_TITLE = "2D Pygame"

# Ширина и высота окна игры
WIDTH = 864
HEIGHT = 700

# размер спрайта в пикселях
SPRITE_SIZE = 32
# количество клеток в ширину и высоту
TILES_X = WIDTH // SPRITE_SIZE
TILES_Y = HEIGHT // SPRITE_SIZE

# цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# типы сущностей
# class EntityTypes(Enum):
#     PLAYER = "P"
#     ENEMY = "X"
#     COLLECTABLE = "C"
#     PROP = "2"
#     NPC = "N"


# Типы клеток
tile_types = {
    "WALL": "1",
    "ROAD": "0",
    "EXIT": "E",
    "START": "P",
    "ENEMY": "X",
    "COLLECTABLE": "C",
}

# пути
PLAYER_SPRITE = r"assets\png\cars\player\blue_coupe_r.png"


# Спрайты взяты из https://minzinn.itch.io/pixelvehicles
