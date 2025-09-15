from classes.entities import Player
import const as C
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

while running:
    # ограничение фпс
    clock.tick(60)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            running = False

    # Рисование спрайтов
    screen.blit(
        PLAYER.sprite,
        (
            (C.WIDTH // 2) - (C.SPRITE_SIZE),
            (C.HEIGHT // 2) - (C.SPRITE_SIZE),
        ),
    )

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
