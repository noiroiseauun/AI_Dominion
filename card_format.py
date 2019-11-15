

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

    def __str__(self):
        '''When you print card, return card name'''
        return self.getName()

    def getName(self): return self.name

    def getType(self): return self.type

    def getCost(self): return self.cost

    def getCoins(self): return self.coins

    def getVp(self): return self.vp

    def isTreasure(self): return "treasure" in self.type

    def isVictory(self): return "victory" in self.type

    def isCurse(self): return "curse" in self.type

def kingdomCards():
    ''' Return a list of all cards in the kingdom
    '''
    kingdom = list()
    kingdom.append(card("curse", ["curse"], 0, coins=0, vp=-1))
    kingdom.append(card("estate", ["victory"], 2, coins=0, vp=1))
    kingdom.append(card("duchy", ["victory"], 5, coins=0, vp=3))
    kingdom.append(card("province", ["victory"], 8, coins=0, vp=6))
    kingdom.append(card("copper", ["treasure"], 0, coins=1, vp=0))
    kingdom.append(card("silver", ["treasure"], 3, coins=2, vp=0))
    kingdom.append(card("gold", ["treasure"], 6, coins=3, vp=0))
    return kingdom

def kingdomCardValues(kingdom):
    kingdomAmounts = dict()
    for card in kingdom:
        if card.getName() == "curse": kingdomAmounts[card.getName()] = 10
        elif card.getName() == "estate": kingdomAmounts[card.getName()] = 8
        elif card.getName() == "duchy": kingdomAmounts[card.getName()] = 8
        elif card.getName() == "province": kingdomAmounts[card.getName()] = 8
        elif card.getName() == "copper": kingdomAmounts[card.getName()] = 46
        elif card.getName() == "silver": kingdomAmounts[card.getName()] = 40
        elif card.getName() == "gold": kingdomAmounts[card.getName()] = 30
    return kingdomAmounts

def startingCards():
    ''' Return the cards the bot starts with
    '''
    deck = list()
    for _ in range(7): deck.append(card("copper", "treasure", 0, coins=1, vp=0))
    for _ in range(3): deck.append(card("estate", "victory", 2, coins=0, vp=1))
    return deck

def allDeckCards(hand, deck, discard, play):
    ''' Start to get all the cards the bot owns into a single list
    '''
    content = list()
    areas = [hand, deck, discard, play]
    for area in areas:
        for card in area: content.append(card.getName())
    return deckContent(content)

def deckContent(deck):
    ''' Create a list of lists of all the elements in the deck
        I.e. [... [copper, 7] ...] indicates there 7 coppers in the deck
        THIS IS THE STATE OF THE BOT
    '''
    tmpSupplyCards = kingdomCards()
    supplyCards = list()
    for card in tmpSupplyCards: supplyCards.append( (card.getName(), 0) )
    for card in deck:
        for index in range(len(supplyCards)):
            if card in supplyCards[index]:
                count = supplyCards[index][1]
                supplyCards[index] = (card, count+1)
                # supplyCard[1] += 1
                break
    # print(supplyCards)
    supplyCards = tuple(supplyCards)
    return supplyCards

def newCard(deck, name):
    if name == "curse":
        deck.append(card("curse", ["curse"], 0, coins=0, vp=-1))
    elif name == "estate":
        deck.append(card("estate", ["victory"], 2, coins=0, vp=1))
    elif name == "duchy":
        deck.append(card("duchy", ["victory"], 5, coins=0, vp=3))
    elif name == "province":
        deck.append(card("province", ["victory"], 8, coins=0, vp=6))
    elif name == "copper":
        deck.append(card("copper", ["treasure"], 0, coins=1, vp=0))
    elif name == "silver":
        deck.append(card("silver", ["treasure"], 3, coins=2, vp=0))
    elif name == "gold":
        deck.append(card("gold", ["treasure"], 6, coins=3, vp=0))
    elif name == "none":
        pass
    return deck

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
