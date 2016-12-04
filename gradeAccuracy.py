import sys
import math
import numpy as np
from sklearn import linear_model
import collections
import dataUtil
import regression
import copy



validationSet_2016_bat = dataUtil.bbref_2016_batters
validationSet_2016_pitch = dataUtil.bbref_2016_pitchers

playerNames = dataUtil.batter_2015_pitchfx.keys()
# remove players who have invalid data or missing data

# print playerNames

validStats = ['OPS+', 'BA', 'BB', 'HR', 'IBB', '3B', 'HBP', 'Rk', 'PA', 'RBI', 'TB', 'AB', 'G', 'H', 'Age', 'R', '2B', 'CS', 'SLG', 'OBP', 'GDP', 'OPS', 'SH', 'SO', 'SB', 'SF']

trout_fake = {'Mike Trout' :{'OPS+': '174', 'BA': '0.315', 'BB': '116', 'HR': '29', 'IBB': '12', '3B': '5', 'HBP': '11', 'Rk': '1485', 'PA': '681', 'RBI': '100', 'TB': '302', 'AB': '549', 'G': '159', 'H': '173', 'Age': '24', 'R': '123', '2B': '32', 'CS': '7', 'SLG': '0.55', 'OBP': '0.441', 'GDP': '5', 'OPS': '0.991', 'SH': '0', 'SO': '137', 'SB': '30', 'SF': '5'}}

trout_real = {'Mike Trout' :{'OPS+': '174', 'BA': '0.315', 'BB': '116', 'HR': '29', 'IBB': '12', '3B': '5', 'HBP': '11', 'Rk': '1485', 'PA': '681', 'RBI': '100', 'TB': '302', 'AB': '549', 'G': '159', 'H': '173', 'Age': '24', 'R': '123', '2B': '32', 'CS': '7', 'SLG': '0.55', 'OBP': '0.441', 'GDP': '5', 'OPS': '0.991', 'SH': '0', 'SO': '137', 'SB': '30', 'SF': '5'}}


batPredictions = {}

batCats = ['HR', 'R', 'RBI', 'SB', 'H', 'G', 'AB']


temp = []
for cat in batCats:
    batPredictions[cat] = {}
    for i, pName in enumerate(playerNames):
        nameSplit = pName.split(' ')
        if pName == "INVALID":
            continue
        # print nameSplit
        # y = regression.predict(nameSplit[0], nameSplit[1], cat)
        y = regression.nextYearPredict(nameSplit[0], nameSplit[1], cat, True)
        if not y:
            playerNames[i] = "INVALID"
            continue

        # print y
        batPredictions[cat][pName] = y


def accuracyCheck(playerName, statCategory):
    testStats = None
    if validationSet_2016_bat.get(playerName, 0):
        yVal = batPredictions[statCategory][playerName]
        percentDiff = abs(float(validationSet_2016_bat[playerName][statCategory]) - yVal + 1)/(yVal + 1)
        # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
        return percentDiff
            

    return 0.0 # Couldn't find player in 2016 data    
    

accuracyCheck("Mike Trsdout", [])

total = []
for cat in batCats:
    for pName in playerNames:
        if pName == "INVALID":
            continue
        # total += accuracyCheck(pName, cat)
        total.append(accuracyCheck(pName, cat))
    # print cat, "accuracy ", total / len(playerNames)
    print cat, "accuracy", np.median(np.array(total))


# PITCHING CATEGORIES

pitcherNames = dataUtil.pitcher_2015_pitchfx.keys()

pitchCats = ['W', 'L', 'ERA', 'H', 'BB', 'SO']
pitchPredictions = {}


for cat in pitchCats:
    pitchPredictions[cat] = {}
    for i, pName in enumerate(pitcherNames):
        nameSplit = pName.split(' ')
        if pName == "INVALID":
            continue
        # y = regression.predict(nameSplit[0], nameSplit[1], cat)
        y = regression.nextYearPredict(nameSplit[0], nameSplit[1], cat)
        if not y:
            pitcherNames[i] = "INVALID"
            continue


        pitchPredictions[cat][pName] = y


def accuracyCheck(playerName, statCategory):
    testStats = None
    if validationSet_2016_pitch.get(playerName, 0):
        yVal = pitchPredictions[statCategory][playerName]
        percentDiff = abs(float(validationSet_2016_pitch[playerName][statCategory]) - yVal + 1)/(yVal + 1)
        # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
        return percentDiff
            

    return 0.0 # Couldn't find player in 2016 data    
    

accuracyCheck("Mike Trsdout", [])

total = []
for cat in pitchCats:
    for pName in pitcherNames:
        if pName == "INVALID":
            continue
        # total += accuracyCheck(pName, cat)
        total.append(accuracyCheck(pName, cat))
    # print cat, "accuracy ", total / len(pitcherNames)
    print cat, "accuracy", np.median(np.array(total))



