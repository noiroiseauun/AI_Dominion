#!/usr/bin/env python

"""
  Author: Adam White, Matthew Schlegel, Mohammad M. Ajallooeian, Sina Ghiassian
  Purpose: Skeleton code for Monte Carlo Exploring Starts Control Agent
           for use on A3 of Reinforcement learning course University of Alberta Fall 2017

"""

from utils import rand_in_range, rand_un
import numpy as np
import pickle
import random

# SAP stands for State-Action-Pair
# F is for Friends :)
gSAPEstimates = dict()
gSAPCurrent = None
gSAPPrevious = None
gEpsilon = 10
gAlpha = 0.5

def agent_init():
    """
    Initialize the variables that need to be reset before each run begins
    Returns: nothing

    """
    global gSAPEstimates, gEpsilon, gAlpha
    # gSAPEstimates = dict()
    # gSAPCurrent = None
    # gSAPPrevious = None
    # 100/1000 = 0.1, the value we want for epsilon
    # gEpsilon = 100
    # gAlpha = 0.75
    return

def agent_start(state):
    """
    Initialize the variavbles that you want to reset before starting a new episode
    Arguments: state: numpy array
    Returns: action: integer
    """
    global gSAPEstimates, gEpsilon, gSAPprevious
    totalDeck = state[0]
    possibleBuys = state[2]
    # print("agent_start possibleBuys: {}".format(possibleBuys))
    buy = bestBuy(totalDeck,possibleBuys, 1)
    gSAPPrevious = (totalDeck, buy)
    return  [buy]


def agent_step(reward, state): # returns NumPy array, reward: floating point, this_observation: NumPy array
    """
    Arguments: reward: floting point, state: integer
    Returns: action: integer
    """
    # Update previous Q, then take next action based on Q
    global gSAPCurrent, gSAPPrevious, gSAPEstimates, gAlpha, gEpsilon
    totalDeck = state[0]
    possibleBuys = state[2]

    # print("agent_step possibleBuys: {}".format(possibleBuys))
    buy = bestBuy(totalDeck,possibleBuys, 1)

    gSAPCurrent = (totalDeck, buy)

    currentValue = gSAPEstimates[gSAPCurrent]
    pastValueUpdated = gSAPEstimates[gSAPPrevious] + gAlpha * (reward + currentValue -  gSAPEstimates[gSAPPrevious])
    gSAPEstimates[gSAPPrevious] = pastValueUpdated
    gSAPPrevious = (totalDeck, buy)

    return [buy]

def agent_end(reward):
    """
    Arguments: reward: floating point
    Returns: Nothing
    """
    # Update state value here, terminal state value is 0
    global gSAPCurrent, gSAPPrevious, gSAPEstimates, gAlpha, gEpsilon
    pastValueUpdated = gSAPEstimates[gSAPPrevious] + gAlpha * (reward + 0 -  gSAPEstimates[gSAPPrevious])
    gSAPEstimates[gSAPPrevious] = pastValueUpdated

    return


def agent_cleanup():
    """
    This function is not used
    """
    # clean up
    return

def agent_message(in_message): # returns string, in_message: string
    global Q
    """
    Arguments: in_message: string
    returns: The value function as a string.
    This function is complete. You do not need to add code here.
    """
    # should not need to modify this function. Modify at your own risk
    if (in_message == 'ValueFunction'):
        return pickle.dumps(np.max(Q, axis=1), protocol=0)
    else:
        return "I don't know what to return!!"


def bestBuy(deck, possibleBuys, numBuys):
    ''' Return the card we are going to buy, normally the greedy buy'''
    # TODO: Multi-buys not implemented; i.e. always assumes 1 buy
    global  gSAPEstimates, gSAPPrevious, gSAPCurrent

    buys = list()   # As in cards we could possibly buy;  parallel array
    values = list() # As in values of the different buys; parallel array
    for card in possibleBuys:
        # print("deck: {}".format(deck))
        # print("card: {}".format(card))
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
