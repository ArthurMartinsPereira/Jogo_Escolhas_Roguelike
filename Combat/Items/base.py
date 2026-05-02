class Item:
    def __init__(self, name, rarity="common"):
        self.name = name
        self.rarity = rarity
        self.passives = []
        self.description = ""
        self.value = 0

    def on_equip(self, player):
        for p in self.passives:
            from Combat.core import add_passive
            add_passive(player, p)

    def on_unequip(self, player):
        for p in self.passives:
            self.remove_passive(player, p)

    def remove_passive(self, player, passive):
        for existing in player.passives:
            if existing["name"] == passive["name"]:
                existing["level"] -= passive.get("level", 1)

                if existing["level"] <= 0:
                    player.passives.remove(existing)
                return
