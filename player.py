from Combat.passives.registry import PASSIVES, MAX_PASSIVE_LEVEL
from Combat.entity import Entity
from Combat.core import DamageType


# =========================
# Stats:
# =========================
class Player(Entity):
    def __init__(self, name):
        # Stats
        super().__init__()
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

        # Hp, Stamina and Life Points
        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp
        self.life = 4
        self.stamina = 4

        self.passives = {}

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

    def spend_stat_points(self):
        pass

    def increase_stat(self, stat, amount=1):
        if self.stat_points >= amount:
            self.stats[stat] += amount
            self.stat_points -= amount

            if stat == "con":
                self.update_hp()
                new_max = self.calculate_life_stamina()
                self.life = min(self.life, new_max)
                self.stamina = min(self.stamina, new_max)
        self.rebuild_passives()

    # =========================
    # Equip Items
    # =========================
    def equip(self, item, slot=None, update=True):
        slot = slot or getattr(item, "slot", None)

        if not slot:
            raise ValueError(f"Item '{item.name}' não tem slot definido")

        if slot not in self.equipament:
            raise ValueError(f"Slot inválido: {slot}")

        # ===== DUAS MÃOS =====
        if hasattr(item, "hands") and item.hands == 2:
            self.unequip("handR", update=False, rebuild=False)
            self.unequip("handL", update=False, rebuild=False)

            self.equipament["handR"] = item
            self.equipament["handL"] = item

        else:
            currentR = self.equipament.get("handR")

            # Remover arma de duas mãos equipada
            if currentR and getattr(currentR, "hands", 1) == 2:
                self.unequip("handR", update=False, rebuild=False)
                self.unequip("handL", update=False, rebuild=False)

            self.unequip(slot, update=False, rebuild=False)
            self.equipament[slot] = item

        self.rebuild_passives()

        if update:
            self.update_hp()

    def equip_artifact(self, item):

        if not self.equipament["artifact1"]:
            self.equipament["artifact1"] = item

        elif not self.equipament["artifact2"]:
            self.equipament["artifact2"] = item

        else:
            self.equipament["artifact1"] = item

        self.rebuild_passives()

        self.update_hp()

    def unequip(self, slot, update=True, rebuild=True):
        item = self.equipament.get(slot)

        if not item:
            return

        self.equipament[slot] = None

        if rebuild:
            self.rebuild_passives()

        if update:
            self.update_hp()

    def rebuild_passives(self):
        self.passives = {}

        processed = set()

        # Passivas de equipamentos
        for item in self.equipament.values():

            if not item:
                continue

            if id(item) in processed:
                continue

            processed.add(id(item))

            for passive in getattr(item, "passives", []):
                self.add_passive_to_pool(passive)

        # Passivas de atributos
        for passive in self.get_stat_passives():
            self.add_passive_to_pool(passive)

    def get_stat_passives(self):
        passives = []

        if self.stats["str"] >= 15:
            passives.append({
                "name": "brutality",
                "level": 1
            })

        if self.stats["str"] >= 25:
            passives.append({
                "name": "brutality",
                "level": 1
            })

        return passives

    def add_passive_to_pool(self, passive):
        name = passive["name"]
        level = passive.get("level", 1)

        if name not in self.passives:
            self.passives[name] = 0

        max_level = PASSIVES.get(
            name, {}
        ).get(
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
    def get_all_damage_instances(self):
        damage_instances = []
        processed = set()

        for slot in ["handR", "handL"]:
            item = self.equipament.get(slot)

            if item and id(item) not in processed:
                if hasattr(item, "get_damage_instances"):
                    damage_instances.extend(
                        item.get_damage_instances(self)
                    )

                processed.add(id(item))

        # Ataque desarmado
        if not damage_instances:
            damage_instances.append({
                "damage": self.stats.get("str", 5),
                "type": DamageType.PHYSICAL
            })

        return damage_instances

    def reset_combat(self):
        super().reset_combat()

        self.max_hp = self.calculate_hp()
        self.hp = self.max_hp

    # =========================
    # State
    # =========================
    def on_death(self):
        self.life = max(0, self.life - 1)
        self.stamina = max(0, self.stamina - 1)

        print("Você perdeu a batalha!")
        print(f"Vida: {self.life} | Stamina {self.stamina}")

    def has_lives(self):
        return self.life > 0

    # def is_alive(self):
        return self.life > 0

    # =========================
    # Inventory
    # =========================

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def use_item(self, item):
        item.use(self)
        self.remove_item(item)

    def show_inventory(self):
        pass