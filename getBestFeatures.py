import sys
import math
import numpy as np
from sklearn import linear_model
import collections
import dataUtil
import regression
import copy
import itertools



validationSet_2016_bat = dataUtil.bbref_2016_batters
validationSet_2016_pitch = dataUtil.bbref_2016_pitchers

# remove players who have invalid data or missing data

# print playerNames

validStats = ['OPS+', 'BA', 'BB', 'HR', 'IBB', '3B', 'HBP', 'Rk', 'PA', 'RBI', 'TB', 'AB', 'G', 'H', 'Age', 'R', '2B', 'CS', 'SLG', 'OBP', 'GDP', 'OPS', 'SH', 'SO', 'SB', 'SF']

trout_fake = {'Mike Trout' :{'OPS+': '174', 'BA': '0.315', 'BB': '116', 'HR': '29', 'IBB': '12', '3B': '5', 'HBP': '11', 'Rk': '1485', 'PA': '681', 'RBI': '100', 'TB': '302', 'AB': '549', 'G': '159', 'H': '173', 'Age': '24', 'R': '123', '2B': '32', 'CS': '7', 'SLG': '0.55', 'OBP': '0.441', 'GDP': '5', 'OPS': '0.991', 'SH': '0', 'SO': '137', 'SB': '30', 'SF': '5'}}

trout_real = {'Mike Trout' :{'OPS+': '174', 'BA': '0.315', 'BB': '116', 'HR': '29', 'IBB': '12', '3B': '5', 'HBP': '11', 'Rk': '1485', 'PA': '681', 'RBI': '100', 'TB': '302', 'AB': '549', 'G': '159', 'H': '173', 'Age': '24', 'R': '123', '2B': '32', 'CS': '7', 'SLG': '0.55', 'OBP': '0.441', 'GDP': '5', 'OPS': '0.991', 'SH': '0', 'SO': '137', 'SB': '30', 'SF': '5'}}


batPredictions = {}

batCats = ['HR', 'R', 'RBI', 'SB', 'H', 'G', 'AB']

batterNames = dataUtil.batter_2015_pitchfx.keys()
pitcherNames = dataUtil.pitcher_2015_pitchfx.keys()

pitchCats = ['W', 'L', 'ERA', 'H', 'BB', 'SO']
pitchPredictions = {}


invalidPlayers = set()


batFeatures = ['AB', 'RBI', 'G', 'H', 'BB', 'HR', 'R', 'SO', '2B', 'SB', 'CS', '3B']
pitchFeatures = ['W','L','G','GS','CG','SHO','SV','IPouts','H','ER','HR','BB','SO','BAOpp','ERA','R']


def generatePredictions(bat = False,features=None):
    categories = pitchCats
    predDict = pitchPredictions
    playerNames = pitcherNames
    if bat:
        predDict = batPredictions
        categories = batCats
        playerNames = batterNames
    for cat in categories:
        predDict[cat] = {}
        for i, pName in enumerate(playerNames):
            nameSplit = pName.split(' ')
            if pName == "INVALID":
                continue
            # print nameSplit
            # y = regression.predict(nameSplit[0], nameSplit[1], cat)
            y = regression.SVRPredict(nameSplit[0], nameSplit[1], cat, bat, myFeatures=features)
            if not y:
                invalidPlayers.add(pName)
                playerNames[i] = "INVALID"
                continue

            predDict[cat][pName] = y
    return predDict



def accuracyCheck(playerName, statCategory, bat = False):
    validationSet = validationSet_2016_pitch
    predictions = pitchPredictions
    if bat:
        validationSet = validationSet_2016_bat
        predictions = batPredictions
    if validationSet.get(playerName, 0):
        yVal = predictions[statCategory][playerName]
        percentDiff = abs(float(validationSet[playerName][statCategory]) - yVal + 1)/(yVal + 1)
        # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
        return percentDiff
            

    return 0.0 # Couldn't find player in 2016 data    
    
def diffCheck(playerName, statCategory, bat = False):
    validationSet = validationSet_2016_pitch
    predictions = pitchPredictions
    if bat:
        validationSet = validationSet_2016_bat
        predictions = batPredictions
    if validationSet.get(playerName, 0):
        yVal = predictions[statCategory][playerName]
        diff = float(validationSet[playerName][statCategory]) - yVal
        # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
        return diff
            

    return 0.0 # Couldn't find player in 2016 data  


accuracyCheck("Mike Trsdout", [])

batDiff = {}
pitchDiff = {}
batPercDiff = []
pitchPercDiff = []

def compare(bat = False):
    hitterOrBatter = "pitcher" if not bat else "batter"
    categories = pitchCats
    names = pitcherNames
    diff = pitchDiff
    percDiff = pitchPercDiff
    predictions = pitchPredictions
    if bat:
        categories = batCats
        names = batterNames
        diff = batDiff
        percDiff = batPercDiff
    for cat in categories:
        diff[cat] = {}
        for name in names:
            if name == "INVALID":
                continue
            diff[cat][name] = diffCheck(name, cat, bat)
            percDiff.append(accuracyCheck(name, cat, bat))

        if hitterOrBatter == "batter":
            hitterOrBatter = " batter"
        print hitterOrBatter, "\t ", cat, " \t error-median: \t ", np.median(np.array(percDiff))
        print hitterOrBatter, "\t ", cat, " \t error-mean: \t ", np.mean(np.array(percDiff))   


# for i in range(1, len(batFeatures)+1):
for j in itertools.combinations(batFeatures, 1):
    features = list(j)
    print features
    generatePredictions(bat=True, features=features)
    compare(bat=True)     

