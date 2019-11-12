
# import numpy as np
# import itertools
import time

class card():
    """docstring for ."""

    def __init__(self, name, type, cost, coins=0, vp=0):
        '''
        Parameters:
            name:   string
            type:   LIST OF STRINGS
            cost:   int
            coins:  int
            vp:     int
        Returns:
            None
        '''
        self.name = name
        self.type = type
        self.cost = cost
        self.coins = coins
        self.vp = vp
        return

    def __str__(self): return self.getName()
    # def print(self): return self.getName()

    def getName(self): return self.name

    def getType(self): return self.type

    def getCost(self): return self.cost

    def getCoins(self): return self.coins

    def getVp(self): return self.vp

    def isTreasure(self): return "treasure" in self.type

    def isVictory(self): return "victory" in self.type

    def isCurse(self): return "curse" in self.type


def testCards():
    x = card("silver", ["treasure"], 3, coins=2)
    # assertEqual(x.getName(), "silver", 'pass')
    # print("name: {} \t type: {} \t cost: {} \t coins: {} \t vp: {}".format(
    #     x.getName(), x.getType(), x.getCost(), x.getCoins(), x.getVp()))
    # print("is {} a treasure? {}".format(x.getName(), x.isTreasure()))
    # print("is {} a victory? {}".format(x.getName(), x.isVictory()))
    return

def main():
    testCards()
    return

if __name__ == '__main__':
    main()
