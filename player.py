class Player:
    def __init__(self):
        # Stats
        self.level = 1
        self.xp = 0
        self.xp_cap = 10
        self.stat_points = 0
        self.stats = {
            "con": 6,
            "str": 6,
            "agi": 6,
            "int": 6,
            "pre": 6
        }

        # Hp, Stamina e Pontos de Vida
        self.max_hp = 80
        self.hp = 80
        self.life = 4
        self.stamina = 4
        self.health = self.calculate_hp()

        # Equipamentos
        self.equipament = {
            "armor": None,
            "handR": None,
            "handL": None,
            "artifact1": None,
            "artifact2": None
        }
        self.inventory = []
        self.gold = 10

    def calculate_hp(self):
        return (self.stats["con"] // 3) * 10

    def update_hp(self):
        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_cap:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_cap
        self.xp_cap += 5
        self.stat_points += 3

        print(f"Level Up! Nível: {self.level}")
        print(f"Pontos disponíveis: {self.stat_points}")

    def increase_stat(self, stat, amount=1):
        if self.stat_points >= amount:
            self.stats[stat] += amount
            self.stat_points -= amount

            if stat == "con":
                self.update_hp()

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def perder_batalha(self):
        self.life -= 1
        self.stamina -= 1
        print("Você perdeu a batalha!")
        print(f"Vida: {self.life} | Stamina {self.stamina}")

    def is_alive(self):
        return self.hp > 0
