class Item:
    def __init__(self, name: str):
        self.name = name


class Potion(Item):
    def __init__(self, name: str, heal_amount: int):
        super().__init__(name)
        self.heal_amount = heal_amount

    def __str__(self):
        return f"{self.name} (Heals: {self.heal_amount} HP)"
