from .base import Item
from .registry import register_item
from Combat.core import DamageType


def get_damage_instances(self, player):
    damage = self.base_damage

    for stat, scale in self.scaling.items():
        damage += player.stats.get(stat, 0) * scale

    return [{
        "damage": damage,
        "type": self.damage_type
    }]


# Registrar Armas:
@register_item("steel_longsword")
class SteelLongsword(Item):
    def __init__(self):
        super().__init__("Espada de Aço Longa", rarity="common")
        self.hands = 2
        self.base_damage = 35

        self.scaling = {
            "str": 0.7,
            "agi": 0.3
        }
        self.damage_type = DamageType.PHYSICAL

        self.passives = [
            {"name": "bleed", "level": 1},
            {"name": "sharpness", "level": 1}
        ]
        self.value = 45
        self.description = "Uma lâmina longa feita de aço, eficiente contra inimigos com pouca armadura."
