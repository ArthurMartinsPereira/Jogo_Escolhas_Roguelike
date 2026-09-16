from .base import Weapon
from .registry import register_item
from Combat.constants import DamageType


# Registrar Armas:
@register_item("iron_sword")
class IronSword(Weapon):
    def __init__(self):
        super().__init__("Espada de Ferro", rarity="common")
        self.hands = 1
        self.base_damage = 13
        self.min_level = 1

        self.scaling = {
            "str": 0.4,
            "agi": 0.4
        }
        self.damage_type = DamageType.PHYSICAL

        self.passives = [
            {"name": "sharpness", "level": 1}
        ]

        self.tags.extend([
            "sword",
            "iron",
            "one_handed"
        ])

        self.value = 16
        self.description = "Uma lâmina simples feita de ferro."

@register_item("steel_longsword")
class SteelLongsword(Weapon):
    def __init__(self):
        super().__init__("Espada de Aço Longa", rarity="common")
        self.hands = 2
        self.base_damage = 35
        self.min_level = 1

        self.scaling = {
            "str": 0.7,
            "agi": 0.3
        }
        self.damage_type = DamageType.PHYSICAL

        self.passives = [
            {"name": "bleed", "level": 1},
            {"name": "sharpness", "level": 1}
        ]

        self.tags.extend([
            "sword",
            "steel",
            "two_handed"
        ])

        self.value = 45
        self.description = "Uma lâmina longa feita de aço, eficiente contra inimigos com pouca armadura."
