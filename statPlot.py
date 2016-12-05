import matplotlib.pyplot as plt
import sys
import math
import numpy as np
from sklearn import linear_model
import collections
import dataUtil
import regression
import copy
import gradeAccuracy as gA




batPred = gA.batPredictions
batDiff = gA.batDiff
batterNames = gA.batterNames
pitchPred = gA.pitchPredictions
pitchDiff = gA.pitchDiff
pitcherNames = gA.pitcherNames
# print pitchPred['W']

def plotCategory(category, bat = False):
    if bat:
        # x = map(int, list(batPred[category].values()))
        x = np.array(batPred[category].values())
        y = np.array(batDiff[category].values())
        print len(batPred[category].keys())
        print len(batDiff[category].keys())

        for key in batPred[category].keys():
            if key not in batDiff[category].keys():
                print key

        # for key in batDiff[category].keys():
        #     if key not in np.array(batPred[category].keys()):
        #         print key
        print "Done"
        print len(x), len(y)
        plt.plot(x, y)

    else:
        pass

plotCategory('HR', True)