
import time
import random
import numpy as np
import card_format
import player_format

maxTurns = 50
phases = ["action", "buy", "cleanup"]
gSAPEstimates = dict() # State-action pair estimates
gSAPPrevious = None # state-action pair previous
gEpsilon = 0.0
gAlpha = 0.0
gConverter = dict()

def firstHand(cards):
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    return (hand, deck, list(), list())

def bestBuy(deck, possibleBuys):
    global  gAlpha, gEpsilon, gSAPEstimates, gSAPPrevious, gConverter
    actions = list()
    for card in possibleBuys:
        # print("card type: {}".format(type(card)))
        # print("deck type: {}".format(type(deck)))
        if (deck, card) not in gSAPEstimates.keys():
            gSAPEstimates[(deck, card)] = 0
        actions.append( (gSAPEstimates[(deck, card)], (deck,card) ) )
    bestActions = max(actions)
    print("actions: {}".format(actions))
    print("bestActions: {}".format(bestActions))
    input("> ")
    return

def actionPhase(hand, deck, discard, play, totalDeck, p1):
    ''' No actions right now '''
    return hand, deck, discard, play, totalDeck, p1

def buyPhase(hand, deck, discard, play, totalDeck, p1):
    global supplyCards
    tmpHand = list()
    while len(hand) > 0:
        card = hand.pop(-1)
        if card.isTreasure():
            p1.changeCoins(card.getCoins())
            play.append(card)
        else: tmpHand.append(card)
    hand = tmpHand
    possibleBuys = list()
    for card in supplyCards:
        if card.getCost() <= p1.getCoins(): possibleBuys.append(card.getName())
    buys = bestBuy(totalDeck, possibleBuys)
    return hand, deck, discard, play, totalDeck, p1

def cleanupPhase(hand, deck, discard, play, totalDeck, p1):

    while len(hand) > 0: discard.append(hand.pop(-1))
    while len(play) > 0: discard.append(play.pop(-1))

    while len(hand) < 5:
        if len(deck) < 1:
            # print("SHUFFLE")
            random.shuffle(discard)
            deck = discard
            discard = list()
        hand.append(deck.pop(-1))
    return hand, deck, discard, play, totalDeck, p1

def initBot():
    global supplyCards, gAlpha, gEpsilon
    random.seed(19)
    p1 = player_format.playerStats(1,1,0,3) # Easy 3 vp for starting
    supplyCards = card_format.kingdomCards()
    cards = card_format.startingCards()
    hand, deck, discard, play = firstHand(cards)
    # 100/1000 = 0.1, the value we want for epsilon
    gEpsilon = 100
    gAlpha = 0.75
    return hand, deck, discard, play, p1

def botPlay(hand, deck, discard, play, p1):
    for turn in range(maxTurns):
        totalDeck = card_format.allDeckCards(hand, deck, discard, play)
        for phase in phases:
            if phase == "action": hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "buy": hand, deck, discard, play, totalDeck, p1 = buyPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "cleanup": hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
            else: print("OH NO")
    return

def main():
    t = time.time()
    hand, deck, discard, play, p1 = initBot()
    botPlay(hand, deck, discard, play, p1)
    print("Total time: {}".format(time.time() - t))

    return

if __name__ == '__main__':
    main()
