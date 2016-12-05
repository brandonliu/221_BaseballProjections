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
invalidNames = gA.invalidPlayers
# print pitchPred['W']

def plotCategory(category, bat = False):
    if bat:
        # x = map(int, list(batPred[category].values()))
        x = []
        y = []
        nameLabels = []
        for pName, val in batPred[category].iteritems():
            if pName not in invalidNames:
                if abs(batDiff[category][pName]) > 20:
                    continue
                nameLabels.append(pName)
                x.append(val)
                y.append(batDiff[category][pName])


        # x = [val for (key, val) in batPred[category].iteritems() if key not in invalidNames]
        # y = [val for (key, val) in batDiff[category].iteritems() if key not in in]
        # x = np.array(batPred[category].values())
        # y = np.array(batDiff[category].values())
        # print len(batPred[category].keys())
        # print len(batDiff[category].keys())

        # for key in batPred[category].keys():
        #     if key not in batDiff[category].keys():
        #         print key

        # for key in batDiff[category].keys():
        #     if key not in np.array(batPred[category].keys()):
        #         print key
        print batPred['HR']["Nolan Arenado"]
        print "Done"
        print len(x), len(y)
        plt.plot(x, y, 'ro')
        for i, xy in enumerate(zip(x, y)):
            plt.annotate(nameLabels[i], xy=xy, textcoords='data')
        plt.xlabel(category, fontsize=18)
        plt.ylabel('residual', fontsize=18)
        plt.show()


        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        # A = -0.75, -0.25, 0, 0.25, 0.5, 0.75, 1.0
        # B = 0.73, 0.97, 1.0, 0.97, 0.88, 0.73, 0.54

        # plt.plot(A,B)
        # for xy in zip(A, B):                                       # <--
        #     ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data') # <--

        # plt.grid()
        # plt.show()

    else:
        pass

plotCategory('HR', True)