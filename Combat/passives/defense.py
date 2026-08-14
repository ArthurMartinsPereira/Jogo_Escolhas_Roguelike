from .registry import register_passive
from Combat.core import Events, DamageType


def block_chance_value(lvl):
    return int(min(0.25, 0.08 * lvl) * 100)

def resistance_value(lvl):
    return int(min(0.8, 0.2 * lvl) * 100)

def elemental_resistance_value(lvl):
    return int(min(0.4, 0.1 * lvl) * 100)

def guardian_value(level):
    return level * 5

def fortitude_value(level):
    return level * 2

@register_passive("fire_resistance",
                  "Reduz dano de fogo em {value}%", value_func=resistance_value)
def fire_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.FIRE:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("ice_resistance",
                  "Reduz dano de gelo em {value}%", value_func=resistance_value)
def ice_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.ICE:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("lightning_resistance",
                  "Reduz dano de raio em {value}%", value_func=resistance_value)
def lightning_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.LIGHTNING:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("magic_resistance",
                  "Reduz dano mágico em {value}%", value_func=resistance_value)
def magic_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.MAGIC:
        ctx.damage *= (1 - min(0.8, 0.2 * level))


@register_passive("physical_resistance",
                  "Reduz dano físico em {value}%", value_func=resistance_value)
def physical_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.PHYSICAL:
        ctx.damage *= (1 - min(0.8, 0.2 * level))

@register_passive("elemental_resistance",
                  "Reduz dano de fogo, gelo e raio em {value}%",
                  value_func=elemental_resistance_value)
def elemental_resistance(event, ctx, level):
    if event == Events.ON_DAMAGE_TAKEN and ctx.type == DamageType.PHYSICAL:
        ctx.damage *= (1 - min(0.4, 0.1 * level))

@register_passive(
    "guardian",
    "Reduz o dano recebido em {value}% enquanto estiver com mais de 75% de vida",
    value_func=guardian_value
)
def guardian(event, ctx, level):

    if event != Events.ON_DAMAGE_TAKEN:
        return

    if ctx.damage <= 0:
        return

    hp_ratio = ctx.target.hp / ctx.target.max_hp

    if hp_ratio > 0.75:
        ctx.damage *= (1 - 0.05 * level)

@register_passive(
    "fortitude",
    "Reduz o dano recebido em {value}% a cada 5 pontos de Constituição.",
    value_func=fortitude_value
)
def fortitude(event, ctx, level):

    if event != Events.ON_DAMAGE_TAKEN:
        return

    if ctx.damage <= 0:
        return

    con = ctx.target.stats.get("con", 0)

    resistance = (con // 5) * (0.02 * level)

    ctx.damage *= (1 - resistance)