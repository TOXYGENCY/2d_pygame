from entities import Player
import const as C
import utils as u
import pygame as pg

# Инициализация Pygame
pg.init()
screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
pg.display.set_caption(C.WINDOW_TITLE)

PLAYER = Player()


# Основной цикл рендера
clock = pg.time.Clock()
running = True

# Заполнение экрана белым цветом
screen.fill(C.WHITE)
u.create_tiles_from_file("levels/level1.txt")

while running:
    # ограничение фпс
    clock.tick(60)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            running = False

    # Рисование спрайтов
    u.render_tiles(screen)

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
