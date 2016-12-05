import dataUtil
import gradeAccuracy

pitcherPredictions =  gradeAccuracy.generatePredictions()
batPredictions = gradeAccuracy.generatePredictions(True)


# calculate MVP
def getMVP():
    featuresToListOfBatterPredictionTuples = {}
    for feature in batPredictions:
        featuresToListOfBatterPredictionTuples[feature] = []
        for player in batPredictions[feature]:
            featuresToListOfBatterPredictionTuples[feature].append((player, batPredictions[feature][player]))
    
    return featuresToListOfBatterPredictionTuples      


featuresToListOfBatterPredictionTuples = getMVP()

featuresToListOfBatterPredictionTuples["H/AB"] = []
for player1 in batPredictions["H"]:
    for player2 in batPredictions["AB"]:
        if player1 == player2:
            featuresToListOfBatterPredictionTuples["H/AB"].append((player1, 
                float(batPredictions["H"][player1])/float(batPredictions["AB"][player1])) )


# for feature in featuresToListOfBatterPredictionTuples:
#     print "LEADERBOARD FOR " + str(feature)
#     print sorted(featuresToListOfBatterPredictionTuples[feature], key=lambda x: x[1], reverse=True)


def getPitchMVP():
    featuresToListOfPitcherPredictionTuples = {}
    for feature in pitcherPredictions:
        featuresToListOfPitcherPredictionTuples[feature] = []
        for player in pitcherPredictions[feature]:
            featuresToListOfPitcherPredictionTuples[feature].append((player, pitcherPredictions[feature][player]))
    
    return featuresToListOfPitcherPredictionTuples 

featuresToListOfPitcherPredictionTuples = getPitchMVP()

for feature in featuresToListOfPitcherPredictionTuples:
    print "LEADERBOARD FOR " + str(feature)
    print sorted(featuresToListOfPitcherPredictionTuples[feature], key=lambda x: x[1], reverse=True)



