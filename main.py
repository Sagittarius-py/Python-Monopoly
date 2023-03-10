import random
from Property import *
from Player import *
import os
import simple_colors
import pickle

fieldNames = [
    "START", "A1", "A2", "A3", "A4", "Railway1", "B1", "B2", "B3", "B4",
    "JAIL", "C1", "Utility1", "C2", "C3", "Railway2", "D1", "D2", "D3", "D4",
    "PARKING", "E1", "E2", "E3", "E4", "Railway3", "F1", "F2", "Utility2", "F3",
    "ToJail", "G1", "G2", "G3", "G4", "Railway4", "H1", "H2", "T3", "H4"
]

notBuyableFieldNames = ["START", "JAIL", "PARKING", "GoToJail"]

playerNames = ["Filip", "Kuba", "Piotrek", "Maciek"]


class MonopolyGame:
    def __init__(self, fieldNames):
        self.currentPlayer = -1
        self.fieldNames = fieldNames

    def createBoard():
        board = []
        i = 0
        startingPrice = 100
        for field in fieldNames:

            if field[0] == "R":
                board.append(Railway(field, 200, 50))
            elif field[0] == "U":
                board.append(Utility(field, 150, 75))
            elif field in notBuyableFieldNames:
                board.append(Property(field))
            else:
                board.append(Road(field, startingPrice,
                                  startingPrice*2))
            startingPrice += 30
            i += 1
        return board

    def createPlayers():
        players = []
        for player in playerNames:
            players.append(Player(player, 15000))
        return players

    def roll_dice():
        return (random.randint(1, 6))


def boardDisplay(board):
    for field in board:
        if hasattr(field, 'owner'):
            if field.owner.name == playerNames[0]:
                print(simple_colors.red(field.name), end=" ")
            elif field.owner.name == playerNames[1]:
                print(simple_colors.green(field.name), end=" ")
            elif field.owner.name == playerNames[2]:
                print(simple_colors.blue(field.name), end=" ")
            elif field.owner.name == playerNames[3]:
                print(simple_colors.yellow(field.name), end=" ")
            else:
                print(field.name, end=" ")
        else:
            print(field.name, end=" ")
    print("\n")


def gameplay(board, players):
    game = 1
    activePlayer = 0
    while game > 0:
        os.system('cls||clear')
        boardDisplay(board)

        # clearing terminal before next player move

        # defining player
        gracz = players[activePlayer]
        # printing info about player
        print("Ruch wykonuje gracz: ", gracz.name,
              "| Posiadane pieni??dze: ", gracz.cash)

        # moving player's position
        move = MonopolyGame.roll_dice()
        gracz.move(move)

        # defining field as player's current standing field
        field = board[gracz.position]

        # printng information about player move
        print(gracz.name, "wyrzuci?? kostk??: ", move,
              ". \n Jego aktualna pozycja to", field.name, "\t")

        # checking if active player have to pay rent to other player
        if field.owner.name != "None" and field.owner != gracz:
            rent_payment = gracz.pay_rent(field)
            if rent_payment:
                print("Pobrana zosta??a op??ata: ", field.rent,
                      "| Posiadane pieni??dze: ", gracz.cash)

            else:
                print(
                    "Przykro nam ale nie masz wystarczaj??cych ??rodk??w na pokrycie op??aty - zbankrutowa??e?? ;_;")

        # Printing information about current field
        if field.name not in notBuyableFieldNames:
            print("\t Cena: ", field.price,
                  "\n\t Op??ata:", field.rent,
                  "\n\t Cena domku:", field.housePrice,
                  "\n\t W??a??ciciel:", field.owner.name,
                  "\n\t Ilo???? domk??w:", field.houses, "\n")

        # asking player what he want to do
        choice = 1
        while choice > 0:
            choice = int(input(
                "Co chcesz teraz zrobi???: \n\t 1) Kup pole \n\t 2) Kup domek \n\t 3) Zapisz gr?? \n\t 0) Zako??cz tur?? \n\t 99) Wyjd?? \n"))

            # if player chooses 1 - buying current field
            if choice == 1:
                if field.name not in notBuyableFieldNames:
                    result = field.buy_property(gracz)
                    if result:
                        print("Uda??o ci si?? kupi?? posiad??o????: ", field.name,
                              "\n Posiadzasz aktualnie: ", gracz.cash)
                        boardDisplay(board)
                    else:
                        print(
                            "Przykro mi, to pole juz do kogo?? nale??y, nie mo??na go kupi?? lub nie masz wystarczaj??co pieni??dzy ;(")

            # if player chooses 2 - buying house on current field
            if choice == 2:
                result = field.buy_house(gracz)
                if result:
                    print("Uda??o ci si?? kupi?? domek! Aktualna liczba domk??w na polu ",
                          field.name, " to ", field.houses)

            if choice == 3:
                filehandler = open("board_save.obj", 'wb')
                pickle.dump(board, filehandler)
                filehandler = open("players_save.obj", 'wb')
                pickle.dump(players, filehandler)

            if choice == 99:
                return True

        # changing player to next
        activePlayer += 1
        if activePlayer > len(playerNames)-1:
            activePlayer = 0


def beforeGame():
    wybor = 1
    while wybor > 0:
        wybor = int(input(
            "Co chcesz robi??? \n\t 1) Rozpocznij gre \n\t 2) Wczytaj gre \n\t 0) Wyjd?? \n"))

        if wybor == 1:
            board = MonopolyGame.createBoard()
            players = MonopolyGame.createPlayers()
            gameplay(board, players)
        if wybor == 2:
            filehandler = open("board_save.obj", 'rb')
            board = pickle.load(filehandler)
            filehandler = open("players_save.obj", 'rb')
            players = pickle.load(filehandler)
            gameplay(board, players)


beforeGame()
