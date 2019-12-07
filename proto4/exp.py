#!/usr/bin/env python

"""
  Author: Adam White, Matthew Schlegel, Mohammad M. Ajallooeian, Andrew
  Jacobsen, Victor Silva, Sina Ghiassian
  Purpose: Implementation of the interaction between the Gambler's problem environment
  and the Monte Carlon agent using RL_glue.
  For use in the Reinforcement Learning course, Fall 2017, University of Alberta

"""

from rl_glue import *  # Required for RL-Glue
RLGlue("env", "agent")

import numpy as np
import pickle, time, random
import matplotlib.pyplot as plt

def plotGraph(array):
    ''' Where we plot the graph '''
    plt.plot(range(len(array)), array,'.b')
    plt.title("SARSA 1 province")
    plt.xlabel("Run")
    plt.ylabel("Turns")
    # print("Alpha: {} \t Epsilon: {}".format(gAlpha, gEpsilon))
    print("Min turns: {}".format(min(array)))
    amount = np.argwhere(array == np.min(array) )
    amount = len(amount.flatten())
    print("Number of times optimal: {}".format(amount))
    print("average turns: {}".format(np.mean(array)))
    # print("state-action space: {}".format(len(gSAPEstimates.keys())))
    plt.show()
    return

def appendInfo(turnList):
    amount = np.argwhere(turnList == np.min(turnList) )
    amount = len(amount.flatten())
    fileObj = open("results2.txt", 'a')
    fileObj.write("--------------------------------------------------------------------------------\n")
    fileObj.write("Epsilon Greedy Single-step SARSA Algorithm on Money Kingdom after {} trials\n".format(len(turnList)))
    fileObj.write("Params: \t Alpha: {} \t Epsilon {}\n".format(gAlpha, gEpsilon))
    fileObj.write("Optimization: \t Min Turns: {} \t # Optimal Runs: {} \t Percentage: {}\n".format(min(turnList), amount, (amount/len(turnList)*100)))
    fileObj.write("Stats: \t Avg Turns: {} \t Median Turns: {}\n".format(np.mean(turnList), np.median(turnList)))
    fileObj.write("Space: \t State-action Space: {}\n".format(len(gSAPEstimates.keys())))
    fileObj.write("--------------------------------------------------------------------------------\n")
    fileObj.close()

def main():
    t = time.time()
    turnList = list()
    for x in range(500):
        hand, deck, discard, play, p1 = initBot(0.8, 150)
        turn = botPlay(hand, deck, discard, play, p1)
        turnList.append(turn)
    plotGraph(turnList)
    print("Total time: {}".format(time.time() - t))
    return

def runExp():
    max_steps = 10000
    num_runs = 10000
    random.seed(19)
    # plotGraph = True
    t = time.time()
    # stepEpisodeList = list()
    turnList = list()
    for run in range(num_runs):
        if run % 1000 == 0: print("run number: {}".format(run))
        # print("run number: {}".format(run))
        RL_init()

        totalSteps = 0
        episodeCounter = 0
        # stepEpisodeList = list()

        steps = 0
        RL_start()
        # RL_start is step 1
        for step in range(1, max_steps):
            action = RL_step()
            if episodeCounter != RL_num_episodes():
                episodeCounter += 1
                # stepEpisodeList.append( (step, episodeCounter) )
                turnList.append(step)
                RL_cleanup()
                break
                # RL_start()
    print("Total time: {}".format(time.time() - t))
    plotGraph(turnList)

if __name__ == "__main__":
    runExp()
