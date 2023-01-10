class Player:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.properties = []
        self.position = 0
        self.bankrupt = 0
        self.railways = 0
        self.utility = 0

    def move(self, dice_roll):
        self.position += dice_roll
        if self.position > 39:
            self.position -= 40
            self.cash += 2000

    def pay_rent(self, property):
        if self.cash >= property.rent:
            self.cash -= property.rent
            property.owner.cash += property.rent
            return True
        else:
            self.bankrupt = 1
            return False
