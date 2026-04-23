def process_status_effects(entity):
    if not hasattr(entity, "status"):
        return

    if "bleed" in entity.status:
        bleed = entity.status["bleed"]

        entity.hp -= bleed["damage"]
        bleed["duration"] -= 1

        if bleed["duration"] <= 0:
            del entity.status["bleed"]