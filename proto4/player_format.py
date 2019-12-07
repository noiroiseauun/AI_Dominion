

class playerStats():

    def __init__(self, actions, buys, coins, vp):
        '''
        Parameters:
            actions:    int
            buys:       int
            coins:      int
            vp:         int
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

def resetStats(player):
    ''' Reset the stats of the bot
    Parameters:
        player (class playerStats): the player whose stats we are reseting

    Returns:
        None
    '''
    while player.getBuys() != 1:
        if player.getBuys() > 1: player.changeBuys(-1)
        else: player.changeBuys(1)
    while player.getActions() != 1:
        if player.getActions() > 1: player.changeActions(-1)
        else: player.getActions(1)
    while player.getCoins() != 0:
        if player.getCoins() > 0: player.changeCoins(-1)
        else: player.changeCoins(1)
    return
