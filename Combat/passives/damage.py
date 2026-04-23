from .registry import register_passive
from Combat.core import Events


def bleed_value(lvl):
    return int((0.03 * lvl) * 100)


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
