class Item:
    def __init__(self, name, slot, scaling_stat, base_power):
        self.name = name
        self.slot = slot
        self.scaling_stat = scaling_stat
        self.base_power = base_power

        self.passives = []

    def get_power(self, player):
        stat_value = player.stats[self.scaling_stat]
        return self.base_power + (stat_value * 0.5)