from entities import Level
import const as C
import pygame as pg

# Инициализация Pygame
pg.init()
screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
pg.display.set_caption(C.WINDOW_TITLE)


# Основной цикл рендера
clock = pg.time.Clock()
running = True

# Заполнение экрана белым цветом
screen.fill(C.WHITE)
level = Level("levels/level1.txt")

while running:
    # ограничение фпс
    clock.tick(8)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            running = False

    # Рисование спрайтов
    level.render_tiles(screen)

    key = pg.key.get_pressed()
    if any(key):
        direction = (0, 0)
        if key[pg.K_w]:
            direction = (0, 1)
        elif key[pg.K_a]:
            direction = (-1, 0)
        elif key[pg.K_s]:
            direction = (0, -1)
        elif key[pg.K_d]:
            direction = (1, 0)

        level.move_player(direction)

    # level.debug()

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
