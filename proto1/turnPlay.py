
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import card_format
import player_format

maxTurns = 1000
phases = ["action", "buy", "cleanup"]
gSAPEstimates = dict() # State-action pair estimates
gSAPPrevious = None # state-action pair previous
gSAPCurrent = None
gEpsilon = 0.0
gAlpha = 0.0

def firstHand(cards):
    ''' Create the first hand to be played; cards are the starting cards
        Returns the hand, deck, discard, and play piles (or locations)
    '''
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    return (hand, deck, list(), list())

def bestBuy(deck, possibleBuys, numBuys):
    ''' Return the card we are going to buy, normally the greedy buy'''
    # TODO: Multi-buys not implemented; i.e. always assumes 1 buy
    global  gSAPEstimates, gSAPPrevious, gSAPCurrent

    buys = list()   # As in cards we could possibly buy;  parallel array
    values = list() # As in values of the different buys; parallel array
    for card in possibleBuys:
        if (deck, card) not in gSAPEstimates.keys(): gSAPEstimates[(deck, card)] = 0
        buys.append(card)
        values.append(gSAPEstimates[(deck, card)])

    randomNum = random.randrange(1000)
    if randomNum < gEpsilon:
        randomIndex = random.randrange( len(buys) )
    else:
        bestActions = np.argwhere(values == np.max(values) )
        bestActions = bestActions.flatten()
        randomIndex = random.choice(bestActions)
    if gSAPCurrent != None:
        gSAPPrevious = gSAPCurrent
    gSAPCurrent = (deck, buys[randomIndex])
    return buys[randomIndex]

def actionPhase(hand, deck, discard, play, totalDeck, p1):
    ''' No actions right now '''
    return hand, deck, discard, play, totalDeck, p1

def buyPhase(hand, deck, discard, play, totalDeck, p1):
    ''' The buy phase for a regular dominion turn'''
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
    totalDeck = card_format.allDeckCards(hand, deck, discard, play)
    return hand, deck, discard, play, totalDeck, p1

def cleanupPhase(hand, deck, discard, play, totalDeck, p1):
    ''' the cleanup phase for a regular dominion turn '''
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

def updateValues(totalDeck):
    ''' math! this is were sarsa is implemented '''
    global gSAPCurrent, gSAPPrevious, gSAPEstimates
    if ("province", 1) in totalDeck: reward = 0
    else: reward = -1
    currentValue = gSAPEstimates[gSAPCurrent]
    pastValueUpdated = gSAPEstimates[gSAPPrevious] + gAlpha * (reward + currentValue -  gSAPEstimates[gSAPPrevious])
    gSAPEstimates[gSAPPrevious] = pastValueUpdated
    return

def initBot():
    ''' where we get the game ready '''
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
    ''' Where the bot walks through each phase of the turn '''
    turn = 0
    for turn in range(maxTurns):
        totalDeck = card_format.allDeckCards(hand, deck, discard, play)
        for phase in phases:
            if phase == "action": hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "buy": hand, deck, discard, play, totalDeck, p1 = buyPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "cleanup": hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
            else: print("OH NO")
        if gSAPPrevious != None:
            # skip providing values the first turn
            updateValues(totalDeck)

        if supplyAmounts["province"] != 8:
            break
    return turn

def plotGraph(array):
    ''' Where we plot the graph '''
    plt.plot(range(len(array)), array,'.b')
    plt.title("SARSA 1 province")
    plt.xlabel("Run")
    plt.ylabel("Turns")
    print("Min turns: {}".format(min(array)))
    amount = np.argwhere(array == np.min(array) )
    amount = len(amount.flatten())
    print("Number of times optimal: {}".format(amount))
    print("average turns: {}".format(np.mean(array)))
    print("state-action space: {}".format(len(gSAPEstimates.keys())))
    plt.show()
    return

def main():
    t = time.time()
    turnList = list()
    for x in range(10000):
        hand, deck, discard, play, p1 = initBot()
        turn = botPlay(hand, deck, discard, play, p1)
        turnList.append(turn)
    plotGraph(turnList)
    print("Total time: {}".format(time.time() - t))

    return

if __name__ == '__main__':
    main()
