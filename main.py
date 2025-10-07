from entities import Level, all_entities
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
win_font = pg.font.SysFont(v.WIN_FONT, v.WIN_FONT_SIZE, True)
lost_font = pg.font.SysFont(v.LOST_FONT, v.LOST_FONT_SIZE, True)


# Рестарт уровня
def restart_level():
    v.show_win_mes = False
    v.show_lost_mes = False
    v.tick_rate = v.DEFAULT_TICK_RATE
    v.lost_mes = "GAME OVER."
    all_entities.clear()
    level = Level(v.selected_level)
    level.moves_score = 0
    print("Level restarted!")
    return level


# Рисование текста
def render_text():
    # Отрисовка счетчика ходов
    text_surface = moves_font.render(
        f"Moves: {level.moves_score}", True, v.TEXT_PRIMARY, v.TEXT_BACKGROUND
    )
    screen.blit(text_surface, (0, 0))

    # Подсказка по управлению
    controls_surface = controls_font.render(
        v.CONTROLS_HINT,
        True,
        v.TEXT_PRIMARY,
        v.TEXT_BACKGROUND,
    )
    screen.blit(controls_surface, (0, v.HEIGHT - v.FONT_SMALL))

    # Отрисовка текста по прохождению уровня
    if v.show_win_mes:
        win_surface = win_font.render(
            v.WIN_MES,
            True,
            v.TEXT_PRIMARY,
            v.TEXT_BACKGROUND,
        )
        screen.blit(
            win_surface, (v.WIDTH // 5, v.HEIGHT // 2 - v.LOST_FONT_SIZE)
        )

    # Отрисовка текста по проигрышу
    if v.show_lost_mes:
        lost_surface = lost_font.render(
            v.lost_mes,
            True,
            v.TEXT_PRIMARY,
            v.TEXT_BACKGROUND,
        )
        screen.blit(
            lost_surface, (v.WIDTH // 7, v.HEIGHT // 2 - v.LOST_FONT_SIZE)
        )


while running:
    # ограничение фпс
    clock.tick(v.tick_rate)

    # Здесь управляем таймером для перемещения остальных сущностей
    if v.entity_move_timer >= v.ENTITY_MOVE_RATE:
        v.entity_move_timer = 0
    else:
        v.entity_move_timer += 1

    # Обработка событий
    events = pg.event.get()
    i = 0
    while i < len(events):
        event = events[i]
        # Выход из игры
        if event.type == pg.QUIT:
            running = False
        i += 1

    # Рисование спрайтов
    level.render_tiles(screen)

    if (
        v.entity_move_timer == v.ENTITY_MOVE_RATE
        and not v.show_lost_mes
        and not v.show_win_mes
    ):
        level.move_entities_on_timer()

    # Рисование текста
    render_text()

    # Обработка нажатий
    key = pg.key.get_pressed()
    if any(key):
        direction = (0, 0)
        if not v.show_lost_mes and not v.show_win_mes:
            if key[pg.K_w]:
                direction = (0, -1)
            elif key[pg.K_a]:
                direction = (-1, 0)
            elif key[pg.K_s]:
                direction = (0, 1)
            elif key[pg.K_d]:
                direction = (1, 0)
        level.move_player(direction)

        if key[pg.K_r]:
            level = restart_level()
        elif key[pg.K_ESCAPE]:
            running = False

    level.debug()

    # Обновление игры
    pg.display.update()


# Выход из Pygame
pg.quit()
