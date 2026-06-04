class Item:
    def __init__(self, name, rarity="common"):
        self.name = name
        self.rarity = rarity
        self.description = ""
        self.value = 0
        self.tags = []


class Equipment(Item):
    def __init__(self, name, rarity="common"):
        super().__init__(name, rarity)
        self.passives = []
        self.slot = None
        self.tags.append("equipment")


class Weapon(Equipment):
    def __init__(self, name, rarity="common"):
        super().__init__(name, rarity)

        self.item_type = "weapon"

        self.slot = "handR"
        self.hands = 1

        self.base_damage = 0
        self.scaling = {}
        self.damage_type = None
        self.tags.append("weapon")

    def get_damage_instances(self, player):
        damage = self.base_damage

        for stat, scale in self.scaling.items():
            damage += player.stats.get(stat, 0) * scale

        damage = int(damage)

        return [{
            "damage": damage,
            "type": self.damage_type
        }]


class Armor(Equipment):
    def __init__(self, name, rarity="common"):
        super().__init__(name, rarity)
        self.slot = "armor"
        self.hp_bonus = 0
        self.item_type = "armor"
        self.tags.append("armor")


class Artifact(Equipment):
    def __init__(self, name, rarity="common"):
        super().__init__(name, rarity)
        self.slot = "artifact"
        self.item_type = "artifact"
        self.tags.append("artifact")


class Consumable(Item):
    def __init__(self, name, rarity="common"):
        super().__init__(name, rarity)
        self.item_type = "consumable"
        self.tags.append("consumable")

    def use(self, player):
        pass
