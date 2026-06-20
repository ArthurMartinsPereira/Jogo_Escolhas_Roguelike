from .base import Enemy
from .registry import register_enemy


@register_enemy("skeleton")
class Skeleton(Enemy):

    def __init__(self):
        super().__init__(
            name="Esqueleto",
            hp=50,
            damage=9,
            passives={
                "bone_armor": 1
            }
        )

        self.xp_reward = 10
        self.gold_reward = 10


@register_enemy("ghoul")
class Ghoul(Enemy):

    def __init__(self):
        super().__init__(
            name="Ghoul",
            hp=65,
            damage=11,
            passives={
                "life_steal": 1
            }
        )

        self.xp_reward = 14
        self.gold_reward = 15


@register_enemy("wraith")
class Wraith(Enemy):

    def __init__(self):
        super().__init__(
            name="Aparição",
            hp=75,
            damage=13,
            passives={
                "dodge": 2,
                "dark_damage": 1
            }
        )

        self.xp_reward = 25
        self.gold_reward = 20