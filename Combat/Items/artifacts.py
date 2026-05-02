from .base import Item
from .registry import register_item


@register_item("vampire_ring")
class AncientCore(Item):
    def __init__(self):
        super().__init__("Anél Vampirico", rarity="rare")

        self.slot = "artifact"
        self.passives = [
            {"name": "lifesteal", "level": 2},
            {"name": "regen", "level": 2}
        ]