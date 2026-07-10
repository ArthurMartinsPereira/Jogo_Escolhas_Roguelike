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
                "swiftness": 1
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

@register_enemy("abomination")
class Abomination(Enemy):

    def __init__(self):
        super().__init__(
            name="Abominação",
            hp=100,
            damage=18,
            passives={
                "physical_resistance": 2,
                "lightning_resistance": 1,
                "regen": 1,
                "berserk": 1
            }
        )

        self.xp_reward = 45
        self.gold_reward = 60