# Registro de Passivas:
PASSIVES = {}
MAX_PASSIVE_LEVEL = 4


def register_passive(name, description="", value_func=None, priority=0, max_level=MAX_PASSIVE_LEVEL):
    def wrapper(func):
        PASSIVES[name] = {
            "func": func,
            "description": description,
            "value_func": value_func,
            "priority": priority,
            "max_level": max_level
        }
        return func

    return wrapper


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


# Eventos | Tipos de Dano
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


# Contexto
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


# Processar Passivas
def process_passives(entity, event, context):
    passives = getattr(entity, "passives", [])

    # Ordena por prioridade
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


# =========================
# PASSIVAS
# =========================

# Defensivas
def resistance_value(lvl):
    return int(min(0.8, 0.2 * lvl) * 100)


def block_chance_value(lvl):
    return int(min(0.25, 0.08 * lvl) * 100)


def lifesteal_value(lvl):
    return int((0.05 * lvl) * 100)


def regen_value(lvl):
    return int((0.02 * lvl) * 100)


def bleed_value(lvl):
    return int((0.03 * lvl) * 100)


@register_passive("block", "Chance de bloquear ataque: {value}%", value_func=block_chance_value, priority=100)
def block(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN:
        import random

        chance = min(0.25, 0.08 * level)

        if random.random() < chance:
            ctx.damage = 0


@register_passive("fire_resistance", "Reduz dano de fogo em {value}%", value_func=resistance_value)
def fire_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.FIRE:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("ice_resistance", "Reduz dano de gelo em {value}%", value_func=resistance_value)
def ice_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.ICE:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("lightning_resistance", "Reduz dano de raio em {value}%", value_func=resistance_value)
def lightning_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.LIGHTNING:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("magic_resistance", "Reduz dano mágico em {value}%", value_func=resistance_value)
def magic_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.MAGIC:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("physical_resistance", "Reduz dano físico em {value}%", value_func=resistance_value)
def physical_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.PHYSICAL:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


# Buffs | Cura
@register_passive("regen", "Regenera {value}% da vida máxima por turno", value_func=regen_value)
def regen(event, ctx, level):
    if event == Events.ON_TICK:
        if ctx.source and hasattr(ctx.source, "max_hp"):
            heal = ctx.source.max_hp * (0.02 * level)
            ctx.source.hp = min(ctx.source.hp_max, ctx.source.hp + heal)


# Ofensivas
@register_passive("life_steal", "Roubo de Vida: {value}% do dano causado", value_func=lifesteal_value)
def life_steal(event, ctx, level):
    if event == Events.ON_HIT:
        if ctx.damage <= 0:
            return

        if ctx.source and hasattr(ctx.source, "hp"):
            heal = ctx.damage * (0.05 * level)
            max_hp = getattr(ctx.source, "max_hp", None)

            if max_hp:
                ctx.source.hp = min(max_hp, ctx.source.hp + heal)
            else:
                ctx.source.hp += heal


@register_passive("bleed", "Chance de aplicar sangramento ({value}% da vida máxima)",
                  value_func=lambda lvl: int((0.03 * lvl) * 100))
def bleed(event, ctx, level):
    if event == Events.ON_HIT:
        import random

        chance = min(0.4, 0.15 * level)

        if ctx.damage <= 0:
            return

        if random.random() < chance:
            target = ctx.target

            if not hasattr(target, "status"):
                target.status = {}

            damage = target.max_hp * (0.03 * level)

            if "bleed" in target.status:
                target.status["bleed"]["damage"] += damage * 0.5
                target.status["bleed"]["duration"] = max(
                    target.status["bleed"]["duration"], 3
                )
            else:
                target.status["bleed"] = {
                    "damage": damage,
                    "duration": 3
                }


def process_status_effects(entity):
    if not hasattr(entity, "status"):
        return

    if "bleed" in entity.status:
        bleed = entity.status["bleed"]

        entity.hp -= bleed["damage"]
        bleed["duration"] -= 1

        if bleed["duration"] <= 0:
            del entity.status["bleed"]


@register_passive("critical_strike", "Chance de crítico +{value}%",
                  value_func=lambda lvl: min(50, lvl * 10),priority=10)
def critical_strike(event, ctx, level):
    if event == Events.ON_ATTACK and ctx.can_crit:
        import random

        crit_chance = min(0.1 * level, 0.5)

        if random.random() < crit_chance:
            ctx.is_crit = True
            ctx.crit_multiplier = min(2.5, 1.5 + 0.4 * level)


@register_passive("_apply_crit", "", priority=20)
def apply_crit(event, ctx, level):
    if event == Events.ON_ATTACK and getattr(ctx, "is_crit", False):
        multiplier = getattr(ctx, "crit_multiplier", 1)

        for dmg in ctx.damage_instances:
            dmg["damage"] *= multiplier


@register_passive("multi_strike", "Chance de ataque extra: {value}% | Máx hits: {level}",
                  value_func=lambda lvl: int((0.10 + 0.05 * lvl) * 100))
def multi_strike(event, ctx, level):
    if event == Events.ON_ATTACK:
        import random

        chance = min(0.30, 0.10 + 0.05 * level)
        hits = 0
        max_hits = min(1 + level, ctx.max_extra_hits)

        for _ in range(max_hits):
            if random.random() < chance:
                hits += 1
                chance *= 0.5
            else:
                break

        ctx.extra_hits = min(ctx.extra_hits + hits, ctx.max_extra_hits)
