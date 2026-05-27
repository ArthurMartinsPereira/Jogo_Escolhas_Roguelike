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
    return name in entity.passives


def get_passive_description(name, level):
    data = PASSIVES.get(name, {})
    desc = data.get("description", "")

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
        passives.items(),
        key=lambda p: PASSIVES.get(p[0], {}).get("priority", 0)
    )

    for name, level in sorted_passives:
        data = PASSIVES.get(name)

        if data:
            func = data["func"]
            func(event, context, level)


def add_passive(entity, new_passive):

    if not hasattr(entity, "passives"):
        entity.passives = {}

    name = new_passive["name"]
    level = new_passive.get("level", 1)

    data = PASSIVES.get(name, {})
    max_level = data.get("max_level", MAX_PASSIVE_LEVEL)

    current = entity.passives.get(name, 0)

    entity.passives[name] = min(
        max_level,
        current + level
    )
