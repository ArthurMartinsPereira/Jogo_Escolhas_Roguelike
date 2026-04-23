from .registry import register_passive
from Combat.core import Events, DamageType


def lifesteal_value(lvl):
    return int((0.05 * lvl) * 100)


def regen_value(lvl):
    return int((0.02 * lvl) * 100)


@register_passive("regen", "Regenera {value}% da vida máxima por turno", value_func=regen_value)
def regen(event, ctx, level):
    if event == Events.ON_TICK:
        if ctx.source and hasattr(ctx.source, "max_hp"):
            heal = ctx.source.max_hp * (0.02 * level)
            ctx.source.hp = min(ctx.source.hp_max, ctx.source.hp + heal)


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
