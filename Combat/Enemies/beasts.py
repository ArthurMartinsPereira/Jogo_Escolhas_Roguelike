from .base import Enemy
from .registry import register_enemy


@register_enemy("wolf")
class Wolf(Enemy):

    def __init__(self):
        super().__init__(
            name="Lobo",
            hp=55,
            damage=8,
            passives={
                "sharpness": 1
            },
            attack_speed=12
        )