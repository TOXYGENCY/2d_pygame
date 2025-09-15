import const as C
import pygame as pg


# Общий класс для всех элементов со спрайтами
class Sprited:
    def __init__(self, sprite_path: str):
        self.sprite_path = sprite_path

        # Загрузка спрайта
        self.sprite = pg.image.load(sprite_path).convert_alpha()


# Сущность
class Entity(Sprited):

    def __init__(self, sprite_path, role: C.EntityTypes):
        super().__init__(sprite_path)
        self.role = role


# Декор
class Prop(Entity):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, C.EntityTypes.PROP)


# Сущность игрока
class Player(Entity):

    def __init__(self):
        super().__init__(C.PLAYER_SPRITE, C.EntityTypes.PLAYER)


# Клетка
class Tile(Sprited):

    def __init__(self, sprite_path, type, entity: Entity = None):
        super().__init__(sprite_path)
        self.type = type
        self.entity = entity
        self.occupied = False
        self.refresh_occupation(self)

    # проверка занятости
    def refresh_occupation(self):
        if self.entity:
            self.occupied = True
        else:
            self.occupied = False
