from .base import Item
from .registry import register_item


@register_item("iron_armor")
class IronArmor(Item):
    def __init__(self):
        super().__init__("Armadura de Ferro")

        self.slot = "armor"
        self.hp_bonus = 80

        self.passives = [
            {"name": "physical_resistance", "level": 1}
        ]

    def on_equip(self, player):
        super().on_equip(player)

        player.max_hp += self.hp_bonus

    def on_unequip(self, player):
        player.max_hp -= self.hp_bonus
        player.hp = min(player.hp, player.max_hp)
