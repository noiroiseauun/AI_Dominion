
import time
import random
import numpy as np
import card_format
import player_format

maxTurns = 1000
phases = ["action", "buy", "cleanup"]
gSAPEstimates = dict() # State-action pair estimates
gSAPPrevious = None # state-action pair previous
gEpsilon = 0.0
gAlpha = 0.0

def firstHand(cards):
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    return (hand, deck, list(), list())

def bestBuy(deck, possibleBuys, numBuys):
    # TODO: Multi-buys not implemented; i.e. always assumes 1 buy
    global  gSAPEstimates, gSAPPrevious
    buys = list()   # As in cards we could possibly buy;  parallel array
    values = list() # As in values of the different buys; parallel array
    for card in possibleBuys:
        if (deck, card) not in gSAPEstimates.keys(): gSAPEstimates[(deck, card)] = 0
        buys.append(card)
        values.append(gSAPEstimates[(deck, card)])
    bestActions = np.argwhere(values == np.max(values) )
    bestActions = bestActions.flatten()
    # Remember that the indexes for alllActions are the actions
    randomIndex = random.choice(bestActions)
    gSAPPrevious = (deck, buys[randomIndex])
    # print("values: {}".format(values))
    # print("buys: {}".format(buys))
    # print("Card Bought: {}".format(buys[randomIndex]))
    # input("> ")
    return buys[randomIndex]

def actionPhase(hand, deck, discard, play, totalDeck, p1):
    ''' No actions right now '''
    return hand, deck, discard, play, totalDeck, p1

def buyPhase(hand, deck, discard, play, totalDeck, p1):
    global supplyCards, supplyAmounts
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
        if card.getCost() <= p1.getCoins() and supplyAmounts[card.getName()] > 0:
            possibleBuys.append(card.getName())
    possibleBuys.append("none") # gotta add that it may be better to buy nothing
    buys = bestBuy(totalDeck, possibleBuys, p1.getBuys())
    if buys != "none": supplyAmounts[buys] -= 1
    discard = card_format.newCard(discard, buys)

    return hand, deck, discard, play, totalDeck, p1

def cleanupPhase(hand, deck, discard, play, totalDeck, p1):

    while len(hand) > 0: discard.append(hand.pop(-1))
    while len(play) > 0: discard.append(play.pop(-1))

    while len(hand) < 5:
        if len(deck) < 1:
            random.shuffle(discard)
            deck = discard
            discard = list()
        hand.append(deck.pop(-1))
    player_format.resetStats(p1)
    return hand, deck, discard, play, totalDeck, p1

def initBot():
    global supplyCards, supplyAmounts, gAlpha, gEpsilon
    random.seed(19)
    p1 = player_format.playerStats(1,1,0,3) # Easy 3 vp for starting
    supplyCards = card_format.kingdomCards()
    supplyAmounts = card_format.kingdomCardValues(supplyCards)
    cards = card_format.startingCards()
    hand, deck, discard, play = firstHand(cards)
    # 100/1000 = 0.1, the value we want for epsilon
    gEpsilon = 100
    gAlpha = 0.75
    return hand, deck, discard, play, p1

def botPlay(hand, deck, discard, play, p1):
    for turn in range(maxTurns):
        # print("t{}".format(turn))
        totalDeck = card_format.allDeckCards(hand, deck, discard, play)
        for phase in phases:
            if phase == "action": hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "buy": hand, deck, discard, play, totalDeck, p1 = buyPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "cleanup": hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
            else: print("OH NO")
        # print("totalDeck after t{}:\n{}".format(turn,totalDeck))
        # print("supplyAmounts:\n{}".format(supplyAmounts))
        # input("> ")
        if supplyAmounts["province"] != 8:
            print("OMG YAY")
            print("totalDeck after t{}: \n{}".format(turn, totalDeck))
            print("supplyAmounts: \n{}".format(supplyAmounts))
            break
    return

def main():
    t = time.time()
    hand, deck, discard, play, p1 = initBot()
    botPlay(hand, deck, discard, play, p1)
    print("Total time: {}".format(time.time() - t))

    return

if __name__ == '__main__':
    main()
