from Combat.passives.registry import PASSIVES, MAX_PASSIVE_LEVEL


class Events:
    GET_ATTACK_SPEED = "get_attack_speed"
    ON_DAMAGE_TAKEN = "on_damage_taken"
    ON_ATTACK = "on_attack"
    ON_HIT = "on_hit"
    ON_TICK = "on_tick"
    ON_BATTLE_START = "on_battle_start"
    ON_KILL = "on_kill"


class DamageType:
    PHYSICAL = "physical"
    BLEED = "bleed"
    MAGIC = "magic"
    FIRE = "fire"
    ICE = "ice"
    DARK = "dark"
    LIGHT = "light"
    LIGHTNING = "lightning"
    POISON = "poison"
    PSYCHIC = "psychic"


def create_passive(name, level=1):
    if name not in PASSIVES:
        raise ValueError(f"Passive '{name}' não existe")
    return {"name": name, "level": level}


def has_passive(entity, name):
    return any(p["name"] == name for p in entity.passives)


def get_passive_description(passive):
    data = PASSIVES.get(passive["name"], {})
    desc = data.get("description", "")
    level = passive.get("level", 1)

    value_func = data.get("value_func")
    value = value_func(level) if value_func else None

    if value is not None:
        desc = desc.format(level=level, value=value)
    else:
        desc = desc.format(level=level)

    return desc + f" (Nv {level})"


class Context:
    def __init__(self, **kwargs):
        self.damage = 0
        self.type = None
        self.source = None
        self.target = None

        self.damage_instances = []
        self.extra_hits = 0
        self.max_extra_hits = 5

        self.can_crit = True
        self.is_crit = False

        self.__dict__.update(kwargs)


def process_passives(entity, event, context):
    passives = getattr(entity, "passives", [])

    sorted_passives = sorted(
        passives,
        key=lambda p: PASSIVES.get(p["name"], {}).get("priority", 0)
    )

    for passive in sorted_passives:
        name = passive.get("name")
        data = PASSIVES.get(name)

        if data:
            func = data["func"]
            level = passive.get("level", 1)
            func(event, context, level)


def add_passive(entity, new_passive):
    if not hasattr(entity, "passives"):
        entity.passives = []

    for p in entity.passives:
        if p["name"] == new_passive["name"]:
            data = PASSIVES.get(p["name"], {})
            max_level = data.get("max_level", MAX_PASSIVE_LEVEL)

            p["level"] = min(max_level, p["level"] + new_passive.get("level", 1))
            return

    entity.passives.append({
        "name": new_passive["name"],
        "level": min(new_passive.get("level", 1), PASSIVES[new_passive["name"]].get("max_level", MAX_PASSIVE_LEVEL))
    })
