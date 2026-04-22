from Combat.passives import Context, Events, process_passives, DamageType


# =========================
# Stats:
# =========================
class Player:
    def __init__(self, name, passives=None):
        # Stats
        self.name = name
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

        # Hp, Stamina and Life Points
        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp
        self.life = 4
        self.stamina = 4

        self.passives = passives if passives else []
        self.status = {}

        self.attack_timer = 0

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

    # =========================
    # Calculations
    # =========================
    def calculate_hp(self):
        return self.stats.get("con", 10) * 10

    def calculate_life_stamina(self):
        return 4 + (self.stats["con"] // 3)

    def update_hp(self):
        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp

    # =========================
    # Leveling
    # =========================
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
                new_max = self.calculate_life_stamina()
                self.life = min(self.life, new_max)
                self.stamina = min(self.stamina, new_max)

    # =========================
    # Combat
    # =========================
    def get_attack_speed(self):
        ctx = Context(source=self, speed=self.stats.get("agi", 10))
        process_passives(self, Events.GET_ATTACK_SPEED, ctx)
        return getattr(ctx, "speed", self.stats.get("agi", 10))

    def process_status_effects(self):
        if "bleed" in self.status:
            bleed = self.status["bleed"]

            self.take_damage(bleed["damage"], DamageType.BLEED)

            bleed["duration"] -= 1
            if bleed["duration"] <= 0:
                del self.status["bleed"]

    def tick(self):
        ctx = Context(source=self, target=self, is_tick=True)
        process_passives(self, Events.ON_TICK, ctx)
        self.process_status_effects()

    def attack(self, target):
        damage_instances = []

        # Basic Attack
        if not self.equipament["handR"] and not self.equipament["handL"]:
            damage_instances.append({
                "damage": self.stats.get("str", 5),
                "type": DamageType.PHYSICAL
            })

        ctx = Context(
            source=self,
            target=target,
            damage_instances=damage_instances
        )

        process_passives(self, Events.ON_ATTACK, ctx)

        # Protections
        damage_instances = getattr(ctx, "damage_instances", [])
        total_hits = max(1, 1 + getattr(ctx, "extra_hits", 0))

        for _ in range(total_hits):
            for dmg in damage_instances:
                final_damage = target.take_damage(
                    dmg["damage"],
                    dmg["type"],
                    source=self
                )

                hit_ctx = Context(
                    damage=final_damage,
                    type=dmg["type"],
                    source=self,
                    target=target
                )

                process_passives(self, Events.ON_HIT, hit_ctx)

    def take_damage(self, dmg, damage_type=DamageType.PHYSICAL, source=None):
        ctx = Context(
            damage=dmg,
            type=damage_type,
            source=source,
            target=self
        )

        process_passives(self, Events.ON_DAMAGE_TAKEN, ctx)
        final_damage = ctx.damage

        self.hp -= final_damage

        if self.hp <= 0:
            self.hp = 0
            self.perder_batalha()

        return final_damage

    # =========================
    # State
    # =========================
    def perder_batalha(self):
        self.life = max(0, self.life - 1)
        self.stamina = max(0, self.stamina - 1)

        print("Você perdeu a batalha!")
        print(f"Vida: {self.life} | Stamina {self.stamina}")

    def is_alive(self):
        return self.life > 0

    def reset_combat(self):
        self.hp = self.max_hp
        self.attack_timer = 0
        self.status.clear()
