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
                "bleed": 1
            },
            attack_speed=13
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
                "poisonous": 1
            },
            attack_speed=12
        )

        self.xp_reward = 8
        self.gold_reward = 5

@register_enemy("snake")
class GiantSnake(Enemy):

    def __init__(self):
        super().__init__(
            name="Cobra Gigante",
            hp=65,
            damage=11,
            passives={
                "poisonous": 3
            },
            attack_speed=13
        )

        self.xp_reward = 18
        self.gold_reward = 15

@register_enemy("bear")
class Bear(Enemy):

    def __init__(self):
        super().__init__(
            name="Urso",
            hp=60,
            damage=15,
            passives={
                "sharpness": 1,
                "physical_resistance": 2
            },
            attack_speed=10
        )

        self.xp_reward = 15
        self.gold_reward = 10