# from abc import ABC, abstractmethod
from const import Roles


# Общий класс для всех элементов со спрайтами
class Sprited:
    def __init__(self, sprite_path: str):
        self.sprite_path = sprite_path


# Сущность
class Entity(Sprited):
    def __init__(self, sprite_path, role: Roles):
        super().__init__(sprite_path)
        self.role = role


# Сущность игрока
class Player(Entity):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, Roles.PLAYER)
