class Entity:
    def __init__(self, name, stats, passives=None):
        self.name = name
        self.stats = stats

        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp

        self.passives = passives if passives else []
        self.effects = []

        self.attack_timer = 0

    def calculate_hp(self):
        return self.stats.get["con", 10] * 10

    def is_alive(self):
        return self.hp > 0

    def get_attack_speed(self):
        return self.stats.get("agi", 10)

    def reset_combat(self):
        self.hp = self.max_hp
        self.attack_timer = 0
        self.effects.clear()

