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

    def __init__(self, role: str):
        # self.assign_sprite(role)
        super().__init__(role)
        self.role = role

    # Автоназначение спрайта по символьному коду её типа
    # def assign_sprite(self, entity_code):
    #     self.sprite_path = C.entity_types[entity_code]


# Декор
class Prop(Entity):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, C.entity_types["2"])


# коллектабл
class Collectable(Entity):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, C.entity_types["C"])
        self.collected = False


# npc (движущийся декор)
class NPC(Entity):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, C.entity_types["N"])


# враг (npc который преследует игрока)
class Enemy(Entity):

    def __init__(self):
        super().__init__(C.entity_types["X"])


# Сущность игрока
class Player(Entity):

    def __init__(self):
        super().__init__(C.entity_types["P"])


# Клетка
class Tile(Sprited):

    def __init__(self, type_code: str):

        self.assign_sprite(type_code)
        super().__init__(self.sprite_path)
        self.type_code = type_code
        self.entity = None
        self.assign_entity()
        self.occupied = False
        self.refresh_occupation()

    # Автоназначение спрайта по символьному коду её типа
    def assign_sprite(self, type_code):
        self.sprite_path = C.tile_types[type_code]

    # Автоназначение сущности
    def assign_entity(self):
        type = self.type_code
        ent = None
        if type == "P":
            ent = Player()
        elif type == "X":
            ent = Enemy()
        elif type == "C":
            ent = Collectable()
        elif type == "2":
            ent = Prop()
        elif type == "N":
            ent = NPC()
        self.entity = ent

    # проверка занятости
    def refresh_occupation(self):
        if self.entity:
            self.occupied = True
        else:
            self.occupied = False
