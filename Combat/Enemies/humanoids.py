from .base import Enemy
from .registry import register_enemy


@register_enemy("goblin")
class Goblin(Enemy):

    def __init__(self):
        super().__init__(
            name="Goblin",
            hp=30,
            damage=5,
            passives={
                "sharpness": 1
            }
        )

        self.xp_reward = 12
        self.gold_reward = 18

@register_enemy("bandit")
class Bandit(Enemy):

    def __init__(self):
        super().__init__(
            name="Bandido",
            hp=60,
            damage=10,
            passives={
                "crit_chance": 1
            }
        )

        self.xp_reward = 12
        self.gold_reward = 18


@register_enemy("mercenary")
class Mercenary(Enemy):

    def __init__(self):
        super().__init__(
            name="Mercenário",
            hp=85,
            damage=12,
            passives={
                "crit_chance": 1,
                "block": 1,
                "multi-strike": 1
            }
        )

        self.xp_reward = 20
        self.gold_reward = 22


@register_enemy("duelist")
class Duelist(Enemy):

    def __init__(self):
        super().__init__(
            name="Duelista",
            hp=70,
            damage=14,
            passives={
                "dodge": 2
            }
        )

        self.xp_reward = 25
        self.gold_reward = 30