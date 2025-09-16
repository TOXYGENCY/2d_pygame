# from enum import Enum

# Константы игры

WINDOW_TITLE = "2D Pygame"

# Ширина и высота окна игры
WIDTH = 900
HEIGHT = 700

# размер спрайта в пикселях
SPRITE_SIZE = 100
# количество клеток в ширину и высоту
TILES_X = WIDTH // SPRITE_SIZE
TILES_Y = HEIGHT // SPRITE_SIZE

# цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# типы сущностей
entity_types = {
    "P": r"assets\png\cars\player\blue_coupe_r.png",
    "X": "EntityTypes.ENEMY",
    "C": "EntityTypes.COLLECTABLE",
    "2": "EntityTypes.PROP",
    "N": "EntityTypes.NPC",
}


# Типы клеток. Содержат пути на спрайты
# tile_types = {
#     "P": "START",
#     "E": "EXIT",
#     "1": "WALL",
#     "0": r"assets\png\roads\road_plain.png",
#     "X": "ENEMY",
#     "C": "COLLECTABLE",
# }

# test
tile_types = {
    "P": r"assets\png\roads\start_plain.png",
    "E": r"assets\png\roads\exit_plain.png",
    "1": r"assets\png\roads\wall_plain.png",
    "0": r"assets\png\roads\road_plain.png",
    "X": r"assets\png\roads\enemy_plain.png",
    # "C": r"assets\png\roads\road_plain.png",
}

# Спрайты взяты из https://minzinn.itch.io/pixelvehicles
