from entities import Level
import vars as v
import pygame as pg

# Инициализация Pygame
pg.init()
screen = pg.display.set_mode((v.WIDTH, v.HEIGHT))
pg.display.set_caption(v.WINDOW_TITLE)

# Основной цикл рендера
clock = pg.time.Clock()
running = True

# Заполнение экрана белым цветом
screen.fill(v.WHITE)
level = Level(v.selected_level)

moves_font = pg.font.SysFont(v.MAIN_FONT, v.FONT_LARGE, True)
controls_font = pg.font.SysFont(v.MAIN_FONT, v.FONT_SMALL, True)


# Рестарт уровня
def restart_level():
    v.show_win_mes = False
    v.show_lost_mes = False
    v.tick_rate = v.DEFAULT_TICK_RATE
    level = Level(v.selected_level)
    return level


while running:
    # ограничение фпс
    clock.tick(v.tick_rate)

    # Обработка событий
    for event in pg.event.get():
        # Выход из игры
        if event.type == pg.QUIT:
            running = False

    # Рисование спрайтов
    level.render_tiles(screen)

    # Рисование текста
    text_surface = moves_font.render(
        f"Moves: {level.moves_score}", True, v.TEXT_PRIMARY, v.TEXT_BACKGROUND
    )
    screen.blit(text_surface, (0, 0))

    controls_surface = controls_font.render(
        v.CONTROLS_HINT,
        True,
        v.TEXT_PRIMARY,
        v.TEXT_BACKGROUND,
    )
    screen.blit(controls_surface, (0, v.HEIGHT - v.FONT_SMALL))

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
        elif key[pg.K_r]:
            level = restart_level()
        elif key[pg.K_ESCAPE]:
            running = False

        level.move_player(direction)

    # level.debug()

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
