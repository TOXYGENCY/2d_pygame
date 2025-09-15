import const as C
import pygame as pg

# Инициализация Pygame
pg.init()
screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
player = pg.image.load(C.PLAYER_SPRITE).convert_alpha()
pg.display.set_caption(C.WINDOW_TITLE)


# Основной цикл рендера
clock = pg.time.Clock()
running = True

# Заполнение экрана белым цветом
screen.fill(C.WHITE)
x = 0
while running:
    # ограничение фпс
    clock.tick(60)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            running = False

    # Рисование красного круга
    screen.blit(player, (x, C.HEIGHT // 2))
    x += 10

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
