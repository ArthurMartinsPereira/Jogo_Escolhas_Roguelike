from Combat.core import Context, Events, process_passives, DamageType
from Combat.status import process_status_effects
from Combat.passives.registry import PASSIVES, MAX_PASSIVE_LEVEL


# =========================
# Stats:
# =========================
class Player:
    def __init__(self, name):
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

        self.passives = {}
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
        base = self.stats.get("con", 10) * 10

        bonus = 0
        for item in self.equipament.values():
            if item and hasattr(item, "hp_bonus"):
                bonus += item.hp_bonus

        return base + bonus

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
    # Equip Items
    # =========================
    def equip(self, item, slot=None, update=False):
        slot = slot or getattr(item, "slot", None)

        if not slot:
            raise ValueError(f"Item '{item.name}' não tem slot definido")

        if slot not in self.equipament:
            raise ValueError(f"Slot inválido: {slot}")

        # ===== DUAS MÃOS =====
        if hasattr(item, "hands") and item.hands == 2:
            self.unequip("handR", update=False)
            self.unequip("handL", update=False)

            self.equipament["handR"] = item
            self.equipament["handL"] = item

        else:
            currentR = self.equipament.get("handR")
            if currentR and getattr(currentR, "hands", 1) == 2:
                self.unequip("handR")

            self.unequip(slot, update=False)
            self.equipament[slot] = item

        self.rebuild_passives()

        self.update_hp()

    def equip_artifact(self, item):
        if not self.equipament["artifact1"]:
            self.equipament["artifact1"] = item
        elif not self.equipament["artifact2"]:
            self.equipament["artifact2"] = item
        else:
            self.unequip("artifact1", update=False)
            self.equipament["artifact1"] = item

        if hasattr(item, "on_equip"):
            item.on_equip(self)

        self.update_hp()

    def unequip(self, slot, update=True):
        item = self.equipament.get(slot)

        if item:
            self.equipament[slot] = None
            self.rebuild_passives()

            if update:
                self.update_hp()

    def rebuild_passives(self):
        self.passives = {}

        processed = set()

        for item in self.equipament.values():

            if not item:
                continue

            if id(item) in processed:
                continue

            processed.add(id(item))

            for passive in item.passives:

                name = passive["name"]
                level = passive.get("level", 1)

                if name not in self.passives:
                    self.passives[name] = 0

                max_level = PASSIVES.get(name, {}).get(
                    "max_level",
                    MAX_PASSIVE_LEVEL
                )

                self.passives[name] = min(
                    max_level,
                    self.passives[name] + level
                )

    # =========================
    # Combat
    # =========================
    def get_attack_speed(self):
        ctx = Context(source=self, speed=self.stats.get("agi", 10))
        process_passives(self, Events.GET_ATTACK_SPEED, ctx)
        return getattr(ctx, "speed", self.stats.get("agi", 10))

    def tick(self):
        ctx = Context(source=self, target=self, is_tick=True)
        process_passives(self, Events.ON_TICK, ctx)
        process_status_effects(self)

    def get_all_damage_instances(self):
        damage_instances = []
        processed = set()

        for slot in ["handR", "handL"]:
            item = self.equipament.get(slot)

            if item and id(item) not in processed:
                if hasattr(item, "get_damage_instances"):
                    damage_instances.extend(item.get_damage_instances(self))
                processed.add(id(item))

        return damage_instances

    def attack(self, target):
        damage_instances = self.get_all_damage_instances()

        # fallback
        if not damage_instances:
            damage_instances.append({
                "damage": self.stats.get("str", 5),
                "type": DamageType.PHYSICAL
            })

        ctx = Context(
            source=self,
            target=target,
            damage_instances=damage_instances
        )

        if not damage_instances:
            return

        process_passives(self, Events.ON_ATTACK, ctx)

        # Protections
        damage_instances = ctx.damage_instances
        total_hits = max(1, 1 + ctx.extra_hits)

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

        self.hp = max(0, self.hp - final_damage)

        if self.hp == 0:
            self.perder_batalha()

        return final_damage

    def reset_combat(self):
        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp
        self.attack_timer = 0
        self.status.clear()

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
