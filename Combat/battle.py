class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.turn = 1

    def player_is_alive(self):
        return self.player.is_alive()

    def enemy_is_alive(self):
        return self.enemy.is_alive()

    def start(self):

        self.player.reset_combat()
        self.enemy.reset_combat()

        while (
                self.player_is_alive()
                and
                self.enemy_is_alive()
        ):
            self.process_turn()

        self.finish()

    def process_turn(self):

        print(f"\n--- Turno {self.turn} ---")

        self.player.attack(self.enemy)

        if self.enemy.is_alive():
            self.enemy.attack(self.player)

        self.print_status()

        self.turn += 1

    def print_status(self):

        print(
            f"{self.player.name}: "
            f"{self.player.hp}/{self.player.max_hp}"
        )

        print(
            f"{self.enemy.name}: "
            f"{self.enemy.hp}/{self.enemy.max_hp}"
        )

    def finish(self):

        if self.player.is_alive():

            self.player.gain_xp(
                self.enemy.xp_reward
            )

            self.player.gold += (
                self.enemy.gold_reward
            )

            print("\nVitória!")
            print(f"+{self.enemy.xp_reward} XP")
            print(f"+{self.enemy.gold_reward} Ouro")

        else:

            print("\nDerrota!")
