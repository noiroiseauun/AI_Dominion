#!/usr/bin/env python

"""
  Author: Adam White, Mohammad M. Ajallooeian, Sina Ghiassian
  Purpose: Code for the Gambler's problem environment from the Sutton and Barto
  Reinforcement Learning: An Introduction Chapter 4.
  For use in the Reinforcement Learning course, Fall 2017, University of Alberta
"""

from utils import rand_norm, rand_in_range, rand_un
import numpy as np
import player_format, card_format
import random

gCurrentState = None
phases = ["cleanup", "action", "buy" ]
player = None
totalDeck = None
supplyCards = None
supplyAmounts = None
totalDeckLists = list()

def env_init():
    global gStartPosition, p1, supplyCards, supplyAmounts, totalDeckLists
    p1 = player_format.playerStats(1,1,0,3) # Easy 3 vp for starting
    totalDeckLists = list()
    supplyCards = card_format.kingdomCards()
    supplyAmounts = card_format.kingdomCardValues(supplyCards)
    cards = card_format.startingCards()
    hand, deck, discard, play = firstHand(cards)
    totalDeck = card_format.allDeckCards(hand, deck, discard, play)
    playAreas = [hand, deck, discard, play]
    possibleBuys = list()
    gStartPosition = [totalDeck, playAreas, possibleBuys]
    return

def env_start():
    """ returns numpy array """
    global gCurrentState, gStartPosition, p1
    gCurrentState = gStartPosition
    totalDeck = gCurrentState[0]
    hand, deck, discard, play = gCurrentState[1]
    possibleBuys = gCurrentState[2]
    hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
    hand, deck, discard, play, totalDeck, p1, buys = buyPhase(hand, deck, discard, play, totalDeck, p1)
    gCurrentState = [totalDeck, [hand, deck, discard, play], buys]
    return gCurrentState


def env_step(action):
    """
    Arguments
    ---------
    action : int
        the action taken by the agent in the current state

    Returns
    -------
    result : dict
        dictionary with keys {reward, state, isTerminal} containing the results
        of the action taken
    """
    global gCurrentState, gTerminalPosition
    global p1
    global totalDeckLists
    reward = -1.0
    isTerminal = False

    totalDeck = gCurrentState[0]
    hand, deck, discard, play = gCurrentState[1]
    possibleBuys = gCurrentState[2]

    for buy in action:
        if buy == "province":
            reward = 1
            isTerminal = True
        if buy != "none":
            supplyAmounts[buy] -= 1
            discard = card_format.newCard(discard, buy)

    totalDeck = card_format.allDeckCards(hand, deck, discard, play)
    hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
    hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
    hand, deck, discard, play, totalDeck, p1, buys = buyPhase(hand, deck, discard, play, totalDeck, p1)
    # for phase in phases:
        # if phase == "action": hand, deck, discard, play, totalDeck, p1 = actionPhase(hand, deck, discard, play, totalDeck, p1)
        # elif phase == "buy": buys = buyPhase(hand, deck, discard, play, totalDeck, p1)
        # elif phase == "cleanup": hand, deck, discard, play, totalDeck, p1 = cleanupPhase(hand, deck, discard, play, totalDeck, p1)
        # else: print("OH NO")

    gCurrentState = [totalDeck, [hand, deck, discard, play], buys]
    totalDeckLists.append(totalDeck)
    result = {"reward": reward, "state": gCurrentState, "isTerminal": isTerminal}
    return result

def env_cleanup():
    #
    global gStartPosition, p1, supplyCards, supplyAmounts, totalDeckLists
    p1 = None
    totalDeck = None
    supplyCards = None
    supplyAmounts = None
    totalDeckLists = list()
    p1 = player_format.playerStats(1,1,0,3) # Easy 3 vp for starting
    totalDeckLists = list()
    supplyCards = card_format.kingdomCards()
    supplyAmounts = card_format.kingdomCardValues(supplyCards)
    cards = card_format.startingCards()
    hand, deck, discard, play = firstHand(cards)
    totalDeck = card_format.allDeckCards(hand, deck, discard, play)
    playAreas = [hand, deck, discard, play]
    possibleBuys = list()
    gStartPosition = [totalDeck, playAreas, possibleBuys]
    return

def env_message(in_message): # returns string, in_message: string
    """
    Arguments
    ---------
    inMessage : string
        the message being passed

    Returns
    -------
    string : the response to the message
    """
    return ""

def firstHand(cards):
    ''' Create the first hand to be played; cards are the starting cards
        Returns the hand, deck, discard, and play piles (or locations)
    '''
    random.shuffle(cards)
    hand = list()
    deck = cards
    for _ in range(5): hand.append(deck.pop(-1))
    return (hand, deck, list(), list())

def actionPhase(hand, deck, discard, play, totalDeck, p1):
    ''' No actions right now '''
    return hand, deck, discard, play, totalDeck, p1

def buyPhase(hand, deck, discard, play, totalDeck, p1):
    ''' The buy phase for a regular dominion turn'''
    global supplyCards, supplyAmounts
    # Little dance of destroying our hand and creating a new one
    # to play all the treasures
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
    return hand, deck, discard, play, totalDeck, p1, possibleBuys

def cleanupPhase(hand, deck, discard, play, totalDeck, p1):
    ''' the cleanup phase for a regular dominion turn '''
    global totalDeckLists
    while len(hand) > 0: discard.append(hand.pop(-1))
    while len(play) > 0: discard.append(play.pop(-1))

    while len(hand) < 5:
        if len(deck) < 1:
            random.shuffle(discard)
            deck = discard
            discard = list()
        if len(deck) < 1:
            print("cleanupPhase deck length: {}".format(len(deck)))
            print("discard length: {}".format(len(discard)))
            print("hand length: {}".format(len(hand)))
            print("play length: {}".format(len(play)))
            print("totalDeck: {}".format(totalDeck))
            print(len(totalDeckLists))
            for x in range(len(totalDeckLists)):
                print(totalDeckLists[x])
                input("> ")
        hand.append(deck.pop(-1))
    player_format.resetStats(p1)
    return hand, deck, discard, play, totalDeck, p1
