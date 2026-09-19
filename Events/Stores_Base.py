import random
from Combat.Items.registry import create_item


class Store:

    def __init__(self, loot_pool, stock_size=3, preferred_tags = None):

        self.loot_pool = loot_pool
        self.stock_size = stock_size
        self.items = []
        self.preferred_tags = preferred_tags or []

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

    def get_sell_price(self, player, item):

        rate = 0.60

        pre = player.stats.get("pre", 6)
        rate += (pre - 6) * 0.01

        if any(tag in self.preferred_tags for tag in item.tags):
            rate += 0.20

        rate = min(rate, 0.90)

        return int(item.value * rate)