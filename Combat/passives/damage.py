from .registry import register_passive
from Combat.core import Events, DamageType


def get_damage_by_type(ctx, damage_type):
    return sum(
        dmg["damage"]
        for dmg in ctx.damage_instances
        if dmg["type"] == damage_type
    )

def bleed_value(lvl):
    return int((0.03 * lvl) * 100)

def sharpness_value(lvl):
    return int(lvl * 10)

def fire_damage_value(level):
    return level * 10

def ice_damage_value(level):
    return level * 10

def lightning_damage_value(level):
    return level * 10

def psychic_damage_value(level):
    return level * 10

def poison_damage_value(level):
    return level * 10

def magic_damage_value(level):
    return level * 10

def dark_damage_value(level):
    return level * 10

def light_damage_value(level):
    return level * 10

def poisonous_damage_value(level):
    return level * 10

def elementalist_value(level):
    return level * 4

def dragon_blood_value(level):
    return level * 20

@register_passive(
    "bleed",
    "Chance de aplicar sangramento ({value}% da vida máxima)",
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

@register_passive(
    "sharpness",
    "Aumenta o dano físico em {value}%",
    value_func=sharpness_value
)
def sharpness(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    for dmg in ctx.damage_instances:

        if dmg["type"] == DamageType.PHYSICAL:

            dmg["damage"] *= (
                1 + 0.10 * level
            )

@register_passive(
    "fire_damage",
    "Adiciona {value}% de dano de fogo",
    value_func=fire_damage_value
)
def fire_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    fire_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": fire_damage,
        "type": DamageType.FIRE
    })

@register_passive(
    "ice_damage",
    "Adiciona {value}% de dano de gelo",
    value_func=ice_damage_value
)
def ice_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    ice_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": ice_damage,
        "type": DamageType.ICE
    })

@register_passive(
    "lightning_damage",
    "Adiciona {value}% de dano de raio",
    value_func=lightning_damage_value
)
def lightning_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    lightning_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": lightning_damage,
        "type": DamageType.LIGHTNING
    })

@register_passive(
    "light_damage",
    "Adiciona {value}% de dano de luz",
    value_func=light_damage_value
)
def light_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    light_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": light_damage,
        "type": DamageType.LIGHT
    })

@register_passive(
    "dark_damage",
    "Adiciona {value}% de dano de escuridão",
    value_func=dark_damage_value
)
def dark_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    dark_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": dark_damage,
        "type": DamageType.DARK
    })

@register_passive(
    "magic_damage",
    "Adiciona {value}% de dano de magia",
    value_func=magic_damage_value
)
def magic_damage(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    magic_damage = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": magic_damage,
        "type": DamageType.MAGIC
    })

@register_passive(
    "poisonous",
    "Adiciona {value}% de dano de veneno",
    value_func=poisonous_damage_value
)
def poisonous(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    base_damage = get_damage_by_type(
        ctx,
        DamageType.PHYSICAL
    )

    poisonous = base_damage * (0.10 * level)

    ctx.damage_instances.append({
        "damage": poisonous,
        "type": DamageType.POISON
    })

@register_passive(
    "elementalist",
    "Aumenta todos os danos elementais em {value}%",
    value_func=elementalist_value
)
def elementalist(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    elemental_types = (
        DamageType.FIRE,
        DamageType.ICE,
        DamageType.LIGHTNING,
        DamageType.LIGHT,
        DamageType.DARK
    )

    for dmg in ctx.damage_instances:

        if dmg["type"] in elemental_types:

            dmg["damage"] *= (
                1 + 0.04 * level
            )

@register_passive(
    "dragon_blood",
    "Aumenta o dano de Fogo, Gelo e Raio em {value}%",
    value_func=dragon_blood_value
)
def dragon_blood(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    dragon_types = (
        DamageType.FIRE,
        DamageType.ICE,
        DamageType.LIGHTNING
    )

    for dmg in ctx.damage_instances:

        if dmg["type"] in dragon_types:

            dmg["damage"] *= (
                1 + 0.20 * level
            )