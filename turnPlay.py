
import time
import random
import card_format
import player_format

maxTurns = 50
phases = ["action", "buy", "cleanup"]
gAlpha = 0.0
gEpsilon = 0.0

def firstHand(cards):
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    return (hand, deck, list(), list())

def bestBuy(deck, possibleBuys):

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
        if card.getCost() <= p1.getCoins(): possibleBuys.append(card)
    x = bestBuy(deck, possibleBuys)
    return hand, deck, discard, play, totalDeck, p1

def cleanupPhase(hand, deck, discard, play, totalDeck, p1):

    while len(hand) > 0: discard.append(hand.pop(-1))
    while len(play) > 0: discard.append(play.pop(-1))

    while len(hand) < 5:
        if len(deck) < 1:
            print("SHUFFLE")
            random.shuffle(discard)
            deck = discard
            discard = list()
        hand.append(deck.pop(-1))
    print("New hand:")
    for card in hand: print(card)

    return hand, deck, discard, play, totalDeck, p1

def main():
    global supplyCards
    random.seed(19)
    p1 = player_format.playerStats(1,1,0,3) # Easy 3 vp for starting
    cards = card_format.startingCards()
    supplyCards = card_format.kingdomCards()
    hand, deck, discard, play = firstHand(cards)
    print("starting hand:")
    for card in hand: print(card)
    for turn in range(maxTurns):
        totalDeck = card_format.allDeckCards(hand, deck, discard, play)
        print("totalDeck: {}".format(totalDeck))
        for phase in phases:
            if phase == "action": hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "buy": hand, deck, discard, play, totalDeck, p1 = buyPhase(hand, deck, discard, play, totalDeck, p1)
            elif phase == "cleanup": hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
            else: print("OH NO")
        print("turn {} done".format(turn))
        input("> ")

    return

if __name__ == '__main__':
    main()
