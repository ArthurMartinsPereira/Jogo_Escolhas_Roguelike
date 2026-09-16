import random
from Combat.Items.registry import create_item


class Store:

    def __init__(self, loot_pool, stock_size=3):

        self.loot_pool = loot_pool
        self.stock_size = stock_size
        self.items = []

    def generate_stock(self, player):

        available = []

        for item_name in self.loot_pool:

            item = create_item(item_name)

            if item.min_level <= player.level:
                available.append(item_name)

        if not available:
            self.items = []
            return

        amount = min(
            self.stock_size,
            len(available)
        )

        selected = random.sample(
            available,
            amount
        )

        self.items = [
            create_item(item_name)
            for item_name in selected
        ]