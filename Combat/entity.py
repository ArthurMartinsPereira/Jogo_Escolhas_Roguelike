from Combat.core import (
    Context,
    Events,
    process_passives,
    DamageType
)

from Combat.status import process_status_effects


class Entity:
    def __init__(self):
        self.passives = {}
        self.status = {}

        self.max_hp = 0
        self.hp = 0

        self.attack_timer = 0

    # =========================
    # Combat
    # =========================

    def get_attack_speed(self):
        ctx = Context(
            source=self,
            speed=getattr(self, "attack_speed", 10)
        )

        process_passives(
            self,
            Events.GET_ATTACK_SPEED,
            ctx
        )

        return ctx.speed

    def tick(self):
        ctx = Context(
            source=self,
            target=self,
            is_tick=True
        )

        process_passives(
            self,
            Events.ON_TICK,
            ctx
        )

        process_status_effects(self)

    def get_all_damage_instances(self):
        return [{
            "damage": getattr(self, "damage", 1),
            "type": DamageType.PHYSICAL
        }]

    def attack(self, target):
        damage_instances = self.get_all_damage_instances()

        if not damage_instances:
            return

        ctx = Context(
            source=self,
            target=target,
            damage_instances=damage_instances
        )

        process_passives(
            self,
            Events.ON_ATTACK,
            ctx
        )

        damage_instances = ctx.damage_instances
        total_hits = max(1, 1 + ctx.extra_hits)

        for _ in range(total_hits):

            for dmg in damage_instances:

                final_damage = target.take_damage(
                    dmg["damage"],
                    dmg["type"],
                    source=self
                )

                hit_ctx = Context(
                    damage=final_damage,
                    type=dmg["type"],
                    source=self,
                    target=target
                )

                process_passives(
                    self,
                    Events.ON_HIT,
                    hit_ctx
                )

    def take_damage(
        self,
        dmg,
        damage_type=DamageType.PHYSICAL,
        source=None
    ):
        ctx = Context(
            damage=dmg,
            type=damage_type,
            source=source,
            target=self
        )

        process_passives(
            self,
            Events.ON_DAMAGE_TAKEN,
            ctx
        )

        final_damage = ctx.damage

        self.hp = max(
            0,
            self.hp - final_damage
        )

        if self.hp == 0:
            self.on_death()

        return final_damage

    # =========================
    # State
    # =========================

    def on_death(self):
        pass

    def reset_combat(self):
        self.hp = self.max_hp
        self.attack_timer = 0
        self.status.clear()

    def is_alive(self):
        return self.hp > 0

