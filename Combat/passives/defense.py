from .registry import register_passive
from Combat.core import Events, DamageType


def block_chance_value(lvl):
    return int(min(0.25, 0.08 * lvl) * 100)


def resistance_value(lvl):
    return int(min(0.8, 0.2 * lvl) * 100)


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
