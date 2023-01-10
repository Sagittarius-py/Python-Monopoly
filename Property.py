class NoneOwner:
    def __init__(self):
        self.name = "None"
        self.cash = 1000000
        self.properties = []
        self.position = 0
        self.in_jail = False


class Property:
    def __init__(self, name):
        self.name = name
        self.owner = NoneOwner()


class Road(Property):
    def __init__(self, name, price, rent):
        self.price = price
        self.rent = rent
        self.housePrice = 100
        self.owner = NoneOwner()
        self.houses = 0
        super().__init__(name)

    def buy_property(self, player):
        if player.cash >= self.price and self.owner.name == "None":
            player.properties.append(self)
            self.owner = player
            player.cash -= self.price

            return True
        else:
            return False

    def buy_house(self, player):
        if player.cash >= self.housePrice and self.owner.name == player.name:
            if self.houses < 4:
                self.houses += 1
                player.cash -= self.housePrice
                self.rent += self.housePrice
            return True
        else:
            return False


class Railway(Road):
    def __init__(self, name, price, rent):
        self.owner = NoneOwner()
        super().__init__(name, price, rent)

    def buy_property(self, player):
        super().buy_property(player)
        self.price *= self.owner.railways
        player.railways += 1
        return True


class Utility(Road):
    def __init__(self, name, price, rent):
        self.owner = NoneOwner()
        super().__init__(name, price, rent)

    def buy_property(self, player):
        super().buy_property(self, player)
        self.rent *= self.owner.utilities
        player.utilities += 1
        return True
