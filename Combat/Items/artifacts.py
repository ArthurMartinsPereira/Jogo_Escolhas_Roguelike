from .base import Artifact
from .registry import register_item


@register_item("vampire_ring")
class AncientCore(Artifact):
    def __init__(self):
        super().__init__("Anél Vampirico", rarity="rare")

        self.slot = "artifact"
        self.passives = [
            {"name": "lifesteal", "level": 2},
            {"name": "regen", "level": 2}
        ]
