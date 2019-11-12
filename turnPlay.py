
import time
import random
import card_format

maxTurns = 50
phases = ["action", "buy", "cleanup"]

class playerStats():

    def __init__(self, actions, buys, coins, vp):
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
        self.actions = actions
        self.buys = buys
        self.coins = coins
        self.vp = vp
        return

    def getActions(self): return self.actions

    def getBuys(self): return self.buys

    def getCoins(self): return self.coins

    def getVp(self): return self.vp

    def changeActions(self, amt=1): self.actions += amt

    def changeBuys(self, amt=1): self.buys += amt

    def changeCoins(self, amt=1): self.coins += amt

    def changeVp(self, amt=1): self.vp += amt


def kingdomCards():
    kingdom = list()
    kingdom.append(card_format.card("curse", ["curse"], 0, coins=0, vp=-1))
    kingdom.append(card_format.card("estate", ["victory"], 2, coins=0, vp=1))
    kingdom.append(card_format.card("duchy", ["victory"], 5, coins=0, vp=3))
    kingdom.append(card_format.card("province", ["victory"], 8, coins=0, vp=6))
    kingdom.append(card_format.card("copper", ["treasure"], 0, coins=1, vp=0))
    kingdom.append(card_format.card("silver", ["treasure"], 3, coins=2, vp=0))
    kingdom.append(card_format.card("gold", ["treasure"], 6, coins=3, vp=0))
    return kingdom

def startingCards():
    deck = list()
    for _ in range(7): deck.append(card_format.card("copper", "treasure", 0, coins=1, vp=0))
    for _ in range(3): deck.append(card_format.card("estate", "victory", 2, coins=0, vp=1))
    return deck

def firstHand(cards):
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    print("Hand: {}".format(len(hand)))
    print("Deck: {}".format(len(deck)))
    for index in range(5):
        print("Index: {} \t Hand: {} \t Deck: {}".format(index, hand[index].getName(), deck[index].getName()))
    return (hand, deck, list(), list())

def actionPhase(hand, deck, discard, play, p1):
    ''' No actions right now '''
    return hand, deck, discard, play

def buyPhase(hand, deck, discard, play, p1):
    tmpHand = hand
    while 
        if card.isTreasure(): p1.changeCoins(card.getCoins())
    return hand, deck, discard, play

def cleanupPhase(hand, deck, discard, play, p1):

    return hand, deck, discard, play

def main():
    p1 = playerStats(1,1,0,3) # Easy 3 vp for starting
    cards = startingCards(p1)
    supplyCards = kingdomCards()
    hand, deck, discard, play = firstHand(cards)

    for turn in range(maxTurns):
        for phase in phases:
            if phase == "action": hand, deck, discard, play, p1 = actionPhase(hand, deck, discard, play, p1)
            elif phase == "buy": hand, deck, discard, play, p1 = buyPhase(hand, deck, discard, play, p1)
            elif phase == "cleanup": hand, deck, discard, play, p1 = cleanupPhase(hand, deck, discard, play, p1)
            else: print("OH NO")


    return

if __name__ == '__main__':
    main()
