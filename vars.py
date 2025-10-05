# Путь выбранного файла уровня относительно main.py
# Если имя файла уровня это level1.txt и лежит в папке levels,
# то путь будет "levels/level1.txt"
selected_level = "levels/level1.txt"

# Константы и глобальные переменные игры
WINDOW_TITLE = "2D Pygame"
CONTROLS_HINT = "Controls: [W], [A], [S], [D], [R]estart, [Esc] close"
WIN_MES = "Congratulations, You Win!"
lost_mes = "GAME OVER."
COLLECTABLE_MES = "You picked up a collectable"

DEFAULT_TICK_RATE = 6
tick_rate = DEFAULT_TICK_RATE

show_lost_mes = False
show_win_mes = False

# Ширина и высота окна игры
WIDTH = 900
HEIGHT = 700

# размер спрайта в пикселях
SPRITE_SIZE = 100

# цвета
WHITE = (255, 255, 255)
DGRAY = (40, 40, 40)

TEXT_PRIMARY = WHITE
TEXT_BACKGROUND = DGRAY

MAIN_FONT = "Consolas"
FONT_LARGE = 30
FONT_SMALL = 16
WIN_FONT = MAIN_FONT
WIN_FONT_SIZE = 40
LOST_FONT = MAIN_FONT
LOST_FONT_SIZE = 30

# типы сущностей
entity_types = {
    "P": r"assets\png\cars\player\blue_coupe_r.png",
    "X": r"assets\png\cars\enemy\red_muscle_r.png",
    "C": r"assets\png\collectables\cash_stack.png",
    "2": r"assets\png\props\tree1.png",
    "N": r"assets\png\cars\npc\npc_r.png",
}

# спрайты игрока
player_sprites = {
    "UP": r"assets\png\cars\player\blue_coupe_u.png",
    "DOWN": r"assets\png\cars\player\blue_coupe_d.png",
    "LEFT": r"assets\png\cars\player\blue_coupe_l.png",
    "RIGHT": r"assets\png\cars\player\blue_coupe_r.png",
}

# спрайты npc
npc_sprites = {
    "UP": r"assets\png\cars\npc\npc_u.png",
    "DOWN": r"assets\png\cars\npc\npc_d.png",
    "LEFT": r"assets\png\cars\npc\npc_l.png",
    "RIGHT": r"assets\png\cars\npc\npc_r.png",
}

# спрайты врага
enemy_sprites = {
    "UP": r"assets\png\cars\enemy\red_muscle_u.png",
    "DOWN": r"assets\png\cars\enemy\red_muscle_d.png",
    "LEFT": r"assets\png\cars\enemy\red_muscle_l.png",
    "RIGHT": r"assets\png\cars\enemy\red_muscle_r.png",
}

# Типы клеток. Содержат пути на спрайты
tile_types = {
    "P": r"assets\png\tiles\start_plain.png",
    "E": r"assets\png\tiles\exit_plain.png",
    "1": r"assets\png\tiles\wall_plain.png",
    "2": r"assets\png\tiles\prop_plain.png",
    "N": r"assets\png\tiles\npc_plain.png",
    "0": r"assets\png\tiles\road_plain.png",
    "X": r"assets\png\tiles\enemy_plain.png",
    "C": r"assets\png\tiles\collectable_plain.png",
}

# Спрайты взяты из https://minzinn.itch.io/pixelvehicles
