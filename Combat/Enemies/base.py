from Combat.entity import Entity
from Combat.core import DamageType


class Enemy(Entity):

    def __init__(
        self,
        name,
        hp,
        damage,
        passives=None,
        attack_speed=10
    ):
        super().__init__()

        self.name = name

        self.max_hp = hp
        self.hp = hp

        self.damage = damage
        self.attack_speed = attack_speed

        self.passives = passives or {}

    def on_death(self):
        pass
