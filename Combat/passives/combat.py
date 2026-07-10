from .registry import register_passive
from Combat.core import Events

def execute_value(level):
    return level * 10

def berserk_value(level):
    return level * 10

@register_passive("critical_strike",
                  "Chance de crítico +{value}%",
                  value_func=lambda lvl: min(50, lvl * 10),priority=10)
def critical_strike(event, ctx, level):
    if event == Events.ON_ATTACK and ctx.can_crit:
        import random

        crit_chance = min(0.1 * level, 0.5)

        if random.random() < crit_chance:
            ctx.is_crit = True
            ctx.crit_multiplier = min(2.5, 1.5 + 0.4 * level)


@register_passive("apply_crit", "", priority=20)
def apply_crit(event, ctx, level):
    if event == Events.ON_ATTACK and getattr(ctx, "is_crit", False):
        multiplier = getattr(ctx, "crit_multiplier", 1)

        for dmg in ctx.damage_instances:
            dmg["damage"] *= multiplier


@register_passive("multi_strike",
                  "Chance de ataque extra: {value}% | Máx hits: {level}",
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


@register_passive(
    "execute",
    "Causa {value}% mais dano contra inimigos abaixo de 30% de vida",
    value_func=execute_value
)
def execute(event, ctx, level):

    if event == Events.ON_ATTACK:

        if ctx.target.hp <= ctx.target.max_hp * 0.3:
            ctx.damage *= (1 + 0.10 * level)


@register_passive(
    "berserk",
    "Aumenta o dano conforme sua vida diminui",
    value_func=berserk_value
)
def berserk(event, ctx, level):

    if event == Events.ON_ATTACK:

        hp_ratio = ctx.source.hp / ctx.source.max_hp

        bonus = (1 - hp_ratio) * (0.10 * level)

        ctx.damage *= (1 + bonus)