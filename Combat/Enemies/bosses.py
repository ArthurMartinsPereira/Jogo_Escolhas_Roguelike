from .base import Enemy
from .registry import register_enemy


@register_enemy("alpha_wolf")
class AlphaWolf(Enemy):

    def __init__(self):
        super().__init__(
            name="Lobo Alfa",
            hp=160,
            damage=18,
            passives={
                "ice_resistance": 3,
                "sharpness": 3,
                "bleed": 2,
                "berserk": 1
            }
        )

        self.xp_reward = 35
        self.gold_reward = 50


@register_enemy("necromancer")
class Necromancer(Enemy):

    def __init__(self):
        super().__init__(
            name="Necromante",
            hp=140,
            damage=15,
            passives={
                "life_steal": 2,
                "dark_damage": 2,
                "regen": 1,
                "magic_resistance": 2
            }
        )

        self.xp_reward = 35
        self.gold_reward = 70