PASSIVES = {}


def register_passive(name):
    def wrapper(func):
        PASSIVES[name] = func
        return func

    return wrapper


class Events:
    ON_DAMAGE_TAKEN = "on_damage_taken"
    ON_ATTACK = "on_attack"
    ON_TICK = "on_tick"


class Context:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def process_passives(entity, event, context):
    for passive in entity.passives:
        func = PASSIVES.get(passive["name"])
        if func:
            level = passive.get("level", 1)
            func(event, context, level)


@register_passive("fire_resistance")
def fire_resistance(event, ctx, level):
    if event == ON_DAMAGE_TAKEN and ctx.type == "fire":
        reduction = min(0.8, 0.25 * level)  # max 80%
        ctx.damage *= (1 - reduction)


@register_passive("ice_resistance")
def ice_resistance(event, ctx, level):
    if event == ON_DAMAGE_TAKEN and ctx.type == "ice":
        reduction = min(0.8, 0.25 * level)  # max 80%
        ctx.damage *= (1 - reduction)


@register_passive("lightning_resistance")
def lightning_resistance(event, ctx, level):
    if event == ON_DAMAGE_TAKEN and ctx.type == "lightning":
        reduction = min(0.8, 0.25 * level)  # max 80%
        ctx.damage *= (1 - reduction)


@register_passive("magic_resistance")
def magic_resistance(event, ctx, level):
    if event == ON_DAMAGE_TAKEN and ctx.type == "magic":
        reduction = min(0.8, 0.25 * level)  # max 80%
        ctx.damage *= (1 - reduction)
