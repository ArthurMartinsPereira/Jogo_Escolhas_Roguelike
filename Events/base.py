class Event:

    title = ""
    description = ""

    unique = False

    def show(self):
        print(f"\n=== {self.title} ===")
        print(self.description)

    def choose(self, *choices):

        for i, choice in enumerate(choices, start=1):
            print(f"{i} - {choice}")

        while True:
            try:
                option = int(input("> "))

                if 1 <= option <= len(choices):
                    return option

            except ValueError:
                pass

            print("Escolha inválida.")

    def test(self, player, stat, difficulty):

        success = player.check_stat(stat, difficulty)

        if success:
            print("Sucesso!")
        else:
            print("Falha!")

        return success

    def start_battle(self, player, enemy_name):

        from Combat.battle import Battle
        from Combat.Enemies.registry import create_enemy

        enemy = create_enemy(enemy_name)

        Battle(player, [enemy]).start()

    def reward_gold(self, player, amount):

        player.gold += amount

        print(f"Você recebeu {amount} moedas.")

    def reward_item(self, player, item):

        player.add_item(item)

        print(f"Você recebeu {item.name}.")

    def reward_xp(self, player, amount):
        player.gain_xp(amount)
        print(f"Você recebeu {amount} XP.")

    def lose_stamina(self, player, amount):
        player.lose_stamina(amount)
        print(f"Você gastou {amount} ponto(s) de stamina.")

    def lose_life(self, player, amount):
        player.lose_life(amount)
        print(f"Você perdeu {amount} ponto(s) de vida.")

    def recover_stamina(self, player, amount):
        player.recover_stamina(amount)
        print(f"Você recuperou {amount} ponto(s) de stamina.")

    def recover_life(self, player, amount):
        player.recover_life(amount)
        print(f"Você recuperou {amount} ponto(s) de vida.")

    def message(self, text):
        print(text)

    def run(self, player):
        pass

