import sys
import math
import numpy as np
from sklearn import linear_model
import collections
import dataUtil
import normalizeRegression
import copy



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

def generatePredictions(bat = False, features=None):
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
            y = normalizeRegression.MLPRegressorPredict(nameSplit[0], nameSplit[1], cat, bat)
            if not y:
                invalidPlayers.add(pName)
                playerNames[i] = "INVALID"
                continue

            predDict[cat][pName] = y
    return predDict




###### PRE_DECOMPOSITION CODE




# temp = []
# for cat in batCats:
#     batPredictions[cat] = {}
#     for i, pName in enumerate(playerNames):
#         nameSplit = pName.split(' ')
#         if pName == "INVALID":
#             continue
#         # print nameSplit
#         # y = regression.predict(nameSplit[0], nameSplit[1], cat)
#         y = regression.nextYearPredict(nameSplit[0], nameSplit[1], cat, True)
#         if not y:
#             playerNames[i] = "INVALID"
#             continue

#         # print y
#         batPredictions[cat][pName] = y



def accuracyCheck(playerName, statCategory, bat = False):
    validationSet = validationSet_2016_pitch
    predictions = pitchPredictions
    if bat:
        validationSet = validationSet_2016_bat
        predictions = batPredictions
    if validationSet.get(playerName, 0):
        yVal = predictions[statCategory][playerName]
        actualValue = float(validationSet[playerName][statCategory])
        gamesPlayed = float(validationSet[playerName]['G'])
        scaleFactor = gamesPlayed/160.0
        yVal = yVal * scaleFactor
        percentDiff = abs(actualValue - yVal + 1)/(actualValue + 1)
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
        actualValue = float(validationSet[playerName][statCategory])
        gamesPlayed = float(validationSet[playerName]['G'])
        scaleFactor = gamesPlayed/160.0
        yVal = yVal * scaleFactor
        diff = abs(actualValue - yVal)
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
        print hitterOrBatter, "\t ", cat, " \t diff-error-median: \t ", np.median(np.array(diff[cat].values()))
        print hitterOrBatter, "\t ", cat, " \t diff-error-mean: \t ", np.mean(np.array(diff[cat].values())) 
        print hitterOrBatter, "\t ", cat, " \t percent-error-median: \t ", np.median(np.array(percDiff))
        print hitterOrBatter, "\t ", cat, " \t percent-error-mean: \t ", np.mean(np.array(percDiff))     


# for i in range(1, len(batFeatures)+1):
#        for j in itertools.combinations(batFeatures, i):
#             features = list(j)
#             generatePredictions(bat=True, features=features)
#             compare(bat=True)

# Generate predictions for pitcher stats and hitter stats
generatePredictions(bat = True)
# generatePredictions(bat = False)

# # Compare predictions for pitcher stats and hitter stats
compare(bat = True)
# compare(bat = False)

# batDiff = {}
# totalPercDiff = []
# for cat in batCats:
#     batDiff[cat] = {}
#     for pName in batterNames:
#         if pName == "INVALID":
#             continue
#         # total += accuracyCheck(pName, cat)
#         batDiff[cat][pName] = diffCheck(pName, cat, True)
#         totalPercDiff.append(accuracyCheck(pName, cat, True))
#     # print cat, "accuracy ", total / len(playerNames)
#     print cat, " accuracy-median: ", np.median(np.array(totalPercDiff))
#     print cat, " accuracy-mean: ", np.mean(np.array(totalPercDiff))



# PITCHING CATEGORIES



# for cat in pitchCats:
#     pitchPredictions[cat] = {}
#     for i, pName in enumerate(pitcherNames):
#         nameSplit = pName.split(' ')
#         if pName == "INVALID":
#             continue
#         # y = regression.predict(nameSplit[0], nameSplit[1], cat)
#         y = regression.nextYearPredict(nameSplit[0], nameSplit[1], cat)
#         if not y:
#             pitcherNames[i] = "INVALID"
#             continue


#         pitchPredictions[cat][pName] = y


# def accuracyCheck(playerName, statCategory):
#     testStats = None
#     if validationSet_2016_pitch.get(playerName, 0):
#         yVal = pitchPredictions[statCategory][playerName]
#         percentDiff = abs(float(validationSet_2016_pitch[playerName][statCategory]) - yVal + 1)/(yVal + 1)
#         # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
#         return percentDiff
            

#     return 0.0 # Couldn't find player in 2016 data    
    
# def diffCheck(playerName, statCategory):
#     testStats = None
#     if validationSet_2016_pitch.get(playerName, 0):
#         yVal = pitchPredictions[statCategory][playerName]
#         diff = float(validationSet_2016_pitch[playerName][statCategory]) - yVal
#         # print playerName, " ", statCategory, " Actual: ", validationSet_2016_bat[playerName][statCategory], "Predicted: ", yVal
#         return diff
            

#     return 0.0 # Couldn't find player in 2016 data  


# accuracyCheck("Mike Trsdout", [])

# pitchDiff = {}
# totalPercDiff = []
# for cat in pitchCats:
#     pitchDiff[cat] = {}
#     for pName in pitcherNames:
#         if pName == "INVALID":
#             continue
#         pitchDiff[cat][pName] = diffCheck(pName, cat)
#         totalPercDiff.append(accuracyCheck(pName, cat))
#     # print cat, "accuracy ", total / len(pitcherNames)
#     print cat, " accuracy-median: ", np.median(np.array(totalPercDiff))
#     print cat, " accuracy-mean: ", np.mean(np.array(totalPercDiff))



