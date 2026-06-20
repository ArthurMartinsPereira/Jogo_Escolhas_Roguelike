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
        self.xp_reward = 8
        self.gold_reward = 10

@register_enemy("dire_wolf")
class DireWolf(Enemy):

    def __init__(self):
        super().__init__(
            name="Lobo Atroz",
            hp=95,
            damage=20,
            passives={
                "sharpness": 2,
                "bleeding": 1
            },
            attack_speed=12
        )
        self.xp_reward = 30
        self.gold_reward = 25

@register_enemy("spider")
class GiantSpider(Enemy):

    def __init__(self):
        super().__init__(
            name="Aranha Gigante",
            hp=35,
            damage=7,
            passives={
                "poison_attack": 1
            }
        )

        self.xp_reward = 8
        self.gold_reward = 5