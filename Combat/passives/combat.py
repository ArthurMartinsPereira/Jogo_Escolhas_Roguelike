from .registry import register_passive
from Combat.core import Events, DamageType

def execute_value(level):
    return level * 10

def berserk_value(level):
    return level * 10

def swiftness_attack(level):
    return level * 5

def swiftness_dodge(level):
    return level * 3

def hunter_value(level):
    return level * 15

def spiked_value(level):
    return level * 10

def thorns_value(level):
    return level * 5

def last_stand_value(level):
    return level * 10

def momentum_value(level):
    return level * 5

def piercing_value(level):
    return level * 10

def double_edge_value(level):
    return level * 10

def glass_cannon_value(level):
    return level * 20

def arcane_resonance_value(level):
    return level * 2

def evasion_mastery_value(level):
    return level * 10

def preys_on_the_weak_value(level):
    return level * 10

def conquer_or_be_conquered_value(level):
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

@register_passive(
    "swiftness",
    "Aumenta a velocidade de ataque em {value}% e a chance de esquiva.",
    value_func=swiftness_attack
)
def swiftness(event, ctx, level):

    if event == Events.ON_ATTACK_SPEED:
        ctx.attack_speed *= (1 + 0.05 * level)

    elif event == Events.ON_DODGE:
        ctx.dodge += 0.03 * level

@register_passive(
    "evasion_mastery",
    "Após esquivar, seu próximo ataque causa +{value}% de dano.",
    value_func=evasion_mastery_value
)
def evasion_mastery(event, ctx, level):

    if event == Events.ON_DODGE:

        ctx.target.evasion_mastery_ready = True

    elif event == Events.ON_ATTACK:

        attacker = ctx.source

        if not getattr(attacker, "evasion_mastery_ready", False):
            return

        for dmg in ctx.damage_instances:
            dmg["damage"] *= (1 + 0.10 * level)

        attacker.evasion_mastery_ready = False

@register_passive(
    "hunter",
    "Causa {value}% mais dano contra Bestas",
    value_func=hunter_value
)
def hunter(event, ctx, level):

    if event == Events.ON_ATTACK:

        if ctx.target.enemy_type == EnemyType.BEAST:
            ctx.damage *= (1 + 0.15 * level)

@register_passive(
    "spiked",
    "Reflete {value}% do dano recebido",
    value_func=spiked_value
)
def spiked(event, ctx, level):

    if event == Events.ON_DAMAGE_TAKEN:

        if ctx.damage <= 0:
            return

        reflected = ctx.damage * (0.10 * level)

        ctx.attacker.take_damage(
            reflected,
            DamageType.PHYSICAL
        )

@register_passive(
    "thorns",
    "Causa {value} de dano físico ao atacante ao receber dano",
    value_func=thorns_value
)
def thorns(event, ctx, level):

    if event != Events.ON_DAMAGE_TAKEN:
        return

    if ctx.damage <= 0:
        return

    damage = 5 * level

    if ctx.attacker is not None:
        ctx.attacker.take_damage(
            damage,
            DamageType.PHYSICAL
        )

@register_passive(
    "last_stand",
    "Reduz o dano recebido em até {value}% conforme sua vida diminui",
    value_func=last_stand_value
)
def last_stand(event, ctx, level):

    if event != Events.ON_DAMAGE_TAKEN:
        return

    if ctx.damage <= 0:
        return

    hp_ratio = ctx.target.hp / ctx.target.max_hp

    bonus = (1 - hp_ratio) * (0.10 * level)

    ctx.damage *= (1 - bonus)

@register_passive(
    "momentum",
    "Cada ataque consecutivo aumenta o dano em {value}%, até {max_value}%",
    value_func=momentum_value
)
def momentum(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    attacker = ctx.source

    if not hasattr(attacker, "momentum_stacks"):
        attacker.momentum_stacks = 0

    max_stacks = level

    attacker.momentum_stacks = min(
        attacker.momentum_stacks + 1,
        max_stacks
    )

    bonus = 0.05 * attacker.momentum_stacks

    for dmg in ctx.damage_instances:
        dmg["damage"] *= (1 + bonus)

@register_passive(
    "piercing",
    "Ignora {value}% da defesa do inimigo",
    value_func=piercing_value
)
def piercing(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    if not hasattr(ctx.target, "defense"):
        return

    ctx.target.defense_modifier = (
        1 - 0.10 * level
    )

@register_passive(
    "double_edge",
    "Aumenta o dano causado em {value}%, mas também aumenta o dano recebido em {value}%.",
    value_func=double_edge_value
)
def double_edge(event, ctx, level):

    if event == Events.ON_ATTACK:

        for dmg in ctx.damage_instances:
            dmg["damage"] *= (1 + 0.10 * level)

    elif event == Events.ON_DAMAGE_TAKEN:

        if ctx.damage <= 0:
            return

        ctx.damage *= (1 + 0.10 * level)

@register_passive(
    "glass_cannon",
    "Aumenta o dano causado em {value}%, mas aumenta o dano recebido em {damage_taken}%.",
    value_func=glass_cannon_value
)
def glass_cannon(event, ctx, level):

    if event == Events.ON_ATTACK:

        for dmg in ctx.damage_instances:
            dmg["damage"] *= (1 + 0.20 * level)

    elif event == Events.ON_DAMAGE_TAKEN:

        if ctx.damage <= 0:
            return

        ctx.damage *= (1 + 0.15 * level)


@register_passive(
    "arcane_resonance",
    "Aumenta o dano mágico em {value}% a cada 5 pontos de Inteligência.",
    value_func=arcane_resonance_value
)
def arcane_resonance(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    int_stat = ctx.source.stats.get("int", 0)

    bonus = (int_stat // 5) * (0.02 * level)

    for dmg in ctx.damage_instances:

        if dmg["type"] == DamageType.MAGIC:
            dmg["damage"] *= (1 + bonus)

@register_passive(
    "death_defiance",
    "Uma vez por combate, sobrevive a um golpe fatal com 1 de vida."
)
def death_defiance(event, ctx, level):

    if event != Events.ON_DAMAGE_TAKEN:
        return

    target = ctx.target

    if getattr(target, "death_defiance_used", False):
        return

    if ctx.damage >= target.hp:

        target.death_defiance_used = True
        ctx.damage = max(0, target.hp - 1)

@register_passive(
    "preys_on_the_weak",
    "Causa {value}% mais dano contra inimigos mais fracos que você.",
    value_func=preys_on_the_weak_value
)
def preys_on_the_weak(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    if ctx.target.max_hp >= ctx.source.max_hp:
        return

    for dmg in ctx.damage_instances:
        dmg["damage"] *= (1 + 0.10 * level)

@register_passive(
    "conquer_or_be_conquered",
    "Causa {value}% mais dano contra inimigos mais fortes que você.",
    value_func=conquer_or_be_conquered_value
)
def conquer_or_be_conquered(event, ctx, level):

    if event != Events.ON_ATTACK:
        return

    if ctx.target.max_hp <= ctx.source.max_hp:
        return

    for dmg in ctx.damage_instances:
        dmg["damage"] *= (1 + 0.10 * level)
