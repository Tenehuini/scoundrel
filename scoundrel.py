import os
import random
import signal
import sys

from collections import namedtuple
from copy import copy


CLEAR_SCREEN = "clear"

CARD_TYPE = namedtuple("Card", "type, value")

# card types
MONSTER = "Monster"
WEAPON = "Weapon"
POTION = "Potion"

# monsters with values from 2 to 14
MONSTERS = [copy(CARD_TYPE(type=MONSTER, value=v)) for v in range(2, 15)]
# weapons with values from 2 to 10
WEAPONS = [copy(CARD_TYPE(type=WEAPON, value=v)) for v in range(2, 11)]
# potions with values from 2 to 10
POTIONS = [copy(CARD_TYPE(type=POTION, value=v)) for v in range(2, 11)]


class Scoundrel:

    def __init__(self):
        self.dungeon = []
        self.room = []
        self.health = 20
        self.equipped = None
        self.last_slayed = None
        self.potions_this_turn = 0

        self.game()
        

    def game(self):
        # create the dungeon
        # we put the monsters two times because there are two of each
        self.dungeon.extend(MONSTERS)
        self.dungeon.extend(MONSTERS)
        self.dungeon.extend(WEAPONS)
        self.dungeon.extend(POTIONS)

        random.shuffle(self.dungeon)

        while not self.endgame():
            print()
            print("Filling the room")
            self.fill_room()
            self.potions_this_turn = 0
            while len(self.room) > 1 or len(self.dungeon) == 0:
                self.print_game()
                self.play()
                if self.health <= 0:
                    break

        print()
        if self.health <= 0:
            print("************************")
            print("Your health dropped to 0")
            print("YOU LOST THE GAME")
        else:
            print("################")
            print("YOU WIN THE GAME")
            print("################")


    def valid_selection(self, selection):
        try:
            card_number = int(selection)
            if card_number - 1 < 0 or card_number - 1 >= len(self.room):
                return False
        except:
            return False
        
        return True


    def manage_selection(self, card):
        print()
        self.room.remove(card)
        if card.type == POTION:
            print("* Consuming potion...")
            if self.potions_this_turn == 0:
                self.potions_this_turn += 1
                self.health += card.value
                if self.health > 20:
                    self.health = 20
            else:
                print("* Already used a potion this turn. Discarding...")
        elif card.type == WEAPON:
            print("* Equipping weapon")
            self.equipped = card
            self.last_slayed = None
        else:
            # is a monster
            if self.last_slayed:
                # monster cannot be blocked if its value is higher than the last blocked monster
                if card.value > self.last_slayed:
                    print(f"* Cannot block monster because it is higher value than lastest blocked monster, losing {card.value} health")
                    self.health -= card.value
                    return
                        
            # if equipped then decide if use the weapon or not
            if self.equipped:
                while True:
                    use_weapon_choice = input("* Use your weapon? y/n: ")
                    if use_weapon_choice.lower().strip() in "yYnN":
                        if use_weapon_choice.lower().strip() == 'y':
                            self.last_slayed = card.value
                            if self.equipped.value < card.value:
                                print(f"* Monster partially blocked, losing {card.value} - {self.equipped.value} = {card.value - self.equipped.value} damage")
                                self.health -= card.value - self.equipped.value
                                return
                            else:
                                print("* Monster blocked")
                                return
                        else:
                            print(f"* Monster not blocked, losing {card.value} health")
                            self.health -= card.value
                            return

            # direct damage
            print(f"* Monster damage: {card.value} health")
            self.health -= card.value


    def play(self):
        while True:
            selection = input("Select card: ")
            if self.valid_selection(selection):
                selected_card = self.room[int(selection) - 1]
                self.manage_selection(selected_card)
                break
            else:
                print("Invalid card")


    def print_game(self):
        print("----------------------------------")
        print(f"Cards left in the dungeon: {len(self.dungeon)}")
        print()

        print("Cards in room:")
        for index, card in enumerate(self.room):
            print(f"{index + 1}: {card.type} with value {card.value}")
        
        print()
        print(f"Health: {self.health}")
        
        if self.equipped:
            print(f"Equipped with weapon of value: {self.equipped.value}")
            if self.last_slayed:
                print(f"Last monster value slayed with this weapon: {self.last_slayed}")
        else:
            print("Equipped with nothing")

        print()


    def fill_room(self):
        while len(self.room) < 4:
            self.room.append(self.dungeon.pop())


    def endgame(self):
        if len(self.dungeon) == 0:
            return True
        if self.health <= 0:
            return True
        return False


def print_rules():
    """Prints the rules"""
    pass


def signal_handler(signal, frame):
    """Signal handler for CTRL+C to clear the screen and exit"""
    os.system(CLEAR_SCREEN)
    sys.exit(0)


def not_valid_initial_choice(choice):
    """Checks that the initial choice is new game (g/G) or read the rules (r/R)"""
    if choice.upper() == "G" or choice.upper() == "R":
        return False
    return True


def main():
    signal.signal(signal.SIGINT, signal_handler)

    choice = input("New Game (G) or Read the Rules (R): ")
    while not_valid_initial_choice(choice):
        input()
    if choice.upper() == "G":
        Scoundrel()
    else:
        print_rules()


if __name__ == "__main__":
    main()