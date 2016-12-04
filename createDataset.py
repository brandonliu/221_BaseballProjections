# Python file to create the data set containing peripheral and traditional statistics

# Current data sets
# - 2015 peripheral statistics
# 2010 - 2015 normal statistics
# 2016 normal statistics
# id information for players in 2010-2015 stats --> need to match that with 2016 stats and 2015 stats

import csv
import sys
import math
import numpy as np
from sklearn import linear_model
import sys
import collections


def main():
    # run on csvfile: 'lahman_csv_2015/core/Batting.csv'
    # run on csvfile: 'lahman_csv_2015/core/Master.csv'

    battingFile = 'lahman_csv_2015/core/Batting.csv'
    masterFile = 'lahman_csv_2015/core/Master.csv'
    pitchingFile = 'lahman_csv_2015/core/Pitching.csv'
    bat_2016File = 'bbref_batters_2016.csv'
    pitch_2016File = 'bbref_pitchers_2016.csv'
    batter_2015_pitchfxFile = 'battersfx2015.csv'
    pitcher_2015_pitchfxFile = 'pitchersfx2015.csv'

    # Values of interest (batters):
    # - year: yearID
    # - games: G
    # - at bats: AB
    # - runs: R
    # - hits: H
    # - batting average: H/AB
    # - home runs: HR
    # - RBIs: RBI
    # - SB: SB


    batterMap = {}
    pitcherMap = {}
    idMap = {}
    # DATASET HANDLING
    # ---------------------
    # I. Create data structures from raw data
    # Each data source will be linked to player by the playerID attribute used in lahman
    # i. Data source: lahman_csv_2015


    # generate data structure to store all player statistics
    # contains player statistics mapped by (playerID_yearID)
    def generatePlayerMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_year_key = str(row['playerID']) + "_" + str(row['yearID'])
                # Delete these values for regression purposes
                del row['playerID']
                del row['yearID']
                del row['teamID']
                del row['lgID']
                map[id_year_key] = row

    # generate data structure to store all batter statistics between 2010 and 2014
    # contains player statistics mapped by (playerID)
    # sums all of the relevant statistics --> we average the numbers later
    newBatterMap = {}
    def generateBatterMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['yearID']) < 2010 or int(row['yearID']) > 2015:
                    # pid = str(row['playerID'])
                    continue
                pid = str(row['playerID'])
                if map.get(pid, 0) == 0:
                    map[pid] = row
                    map[pid]['numYears'] = 1
                else:
                    map[pid]['numYears'] += 1
                    map[pid]['HR'] = int(map[pid]['HR']) + int(row['HR'])
                    map[pid]['G'] = int(map[pid]['G']) + int(row['G'])
                    map[pid]['R'] = int(map[pid]['R']) + int(row['R'])
                    map[pid]['AB'] = int(map[pid]['AB']) + int(row['AB'])
                    map[pid]['H'] = int(map[pid]['H']) + int(row['H'])
                    map[pid]['RBI'] = int(map[pid]['RBI']) + int(row['RBI'])
                    map[pid]['SB'] = int(map[pid]['SB']) + int(row['SB'])

    # Values of interest (pitchers):
    # - year: yearID
    # - games started: GS
    # - walks: BB
    # - ERA: ERA
    # - ERs: ER
    # - wins: W
    # - losses: L
    # - innings: IPouts / 3
    # - hits: H


    # generate data structure to store all pitcher statistics between 2010 and 2014
    # contains player statistics mapped by (playerID)
    # sums all of the relevant statistics --> we average the numbers later
    newPitcherMap = {}
    def generatePitcherMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['yearID']) < 2010 or int(row['yearID']) > 2015:
                    continue
                pid = str(row['playerID'])
                if map.get(pid, 0) == 0:
                    map[pid] = row
                    map[pid]['numYears'] = 1

                else:
                    map[pid]['numYears'] += 1
                    map[pid]['GS'] = int(map[pid]['GS']) + int(row['GS'])
                    map[pid]['W'] = int(map[pid]['W']) + int(row['W'])
                    map[pid]['L'] = int(map[pid]['L']) + int(row['L'])
                    map[pid]['ER'] = int(map[pid]['ER']) + int(row['ER'])
                    map[pid]['H'] = int(map[pid]['H']) + int(row['H'])
                    map[pid]['IPouts'] = float(map[pid]['IPouts']) + float(row['IPouts'])
                    map[pid]['BB'] = int(map[pid]['BB']) + int(row['BB'])


    # generates the tables of ocrresponding ID values for each player
    idNamePairs = {}
    def generateIDTable(map = idMap):
        with open(masterFile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pid = str(row['playerID'])
                map[pid] = row
                playerName = row['nameFirst'] + " " + row['nameLast']
                # if playerName == 'J. D. Martinez' or row['nameGiven'] == 'Julio Daniel':
                #     playerName = 'J.D. Martinez'
                if playerName not in idNamePairs:
                    idNamePairs[playerName] = [(pid, row['debut'])]
                else:
                    idNamePairs[playerName].append((pid, row['debut']))

    
    # ii. Data source: bbref_2016
    def generate2016Data(filename2016, newMap):
        with open(filename2016) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                if name[len(name) -1] == '*':
                    name = name[:len(name)-1]
                if name in newMap:
                    if row['Tm'] != 'TOT':
                        continue
                del row['Name']
                del row['Tm']
                del row['Lg']
                newMap[name] = row



    # iii. Data source: pitchfx
    def generatePitchFXData(filenamePitchfx, newMap):
        with open(filenamePitchfx) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                del row['Name']
                del row['Team']
                newMap[name] = row


    print "Generate data frame from bbref 2016 data...."
    bbref_2016_batters = {}
    bbref_2016_pitchers = {}
    generate2016Data(bat_2016File, bbref_2016_batters)
    generate2016Data(pitch_2016File, bbref_2016_pitchers)

    print "...."
    print "Generating data frame from Lahman batter dataset"
    # Create all of the maps
    generatePlayerMap(battingFile, batterMap)
    print "Generating data frame from Lahman pitcher dataset"
    generatePlayerMap(pitchingFile, pitcherMap)
    generateIDTable()
    print "..."
    newBatterMap = {}
    newPitcherMap = {}
    generateBatterMap(battingFile, newBatterMap)
    generatePitcherMap(pitchingFile, newPitcherMap)

    print "Generating data frames from Fangraphs 2015 advanced statistics dataset"
    batter_2015_pitchfx = {}
    pitcher_2015_pitchfx = {}
    generatePitchFXData(batter_2015_pitchfxFile, batter_2015_pitchfx)
    generatePitchFXData(pitcher_2015_pitchfxFile, pitcher_2015_pitchfx)
    print "..."
    print "Complete! Finished loading data."

    playerNames = set()
    dupPlayers = []
    for key, val in newBatterMap.iteritems():
        pName = idMap[key]['nameFirst'] + " " + idMap[key]['nameLast']
        if pName not in batter_2015_pitchfx:
            continue
        if pName in playerNames:
            dupPlayers.append(pName)
        playerNames.add(pName)

    for key, val in newPitcherMap.iteritems():
        pName = idMap[key]['nameFirst'] + " " + idMap[key]['nameLast']
        if pName not in pitcher_2015_pitchfx:
            continue
        if pName in playerNames:
            dupPlayers.append(pName)
        playerNames.add(pName)


    # Create the methods to access player data when given a player name

    # Input: A string of a player's name (e.g. Mike Trout)
    # If there are duplicates found, then it will prompt the user for which
    # player they are interested in.

    # Normalize flag will add in fake years even if a player didn't play
    # Raw will return a dict but raw will return only numbers in list form
    def getPlayerInformation(playerName, normalize = False, raw = False):
        # Get 2016 information
        info2016 = None
        playerCurrent = False
        batter = False
        if playerName in bbref_2016_pitchers:
            info2016 = bbref_2016_pitchers[playerName]
            playerCurrent = True
        elif playerName in bbref_2016_batters:
            batter = True
            info2016 = bbref_2016_batters[playerName]
            playerCurrent = True
        
        if not playerCurrent:
            print "Player %s no longer active." % playerName
            return None, None, None
        playerPitchFxData = None
        if playerName in pitcher_2015_pitchfx and not batter:
            playerPitchFxData = pitcher_2015_pitchfx[playerName]
        elif playerName in batter_2015_pitchfx and batter:
            playerPitchFxData = batter_2015_pitchfx[playerName]
        player_2010to2015 = None
        if playerName in idNamePairs:
            playerIDInfo = idNamePairs[playerName][0] # Just takes the first player it finds
            pid = playerIDInfo[0]
            player_2010to2015 = {}
            if not batter:
                # If we don't find data for that year, we just replace it with duplicate data from another year
                tempData = {}
                yearsMissing = []
                for year in range(2010, 2015 + 1):
                    keyID = str(pid) + "_" + str(year)
                    if keyID in batterMap:
                        player_2010to2015[str(year)] = pitcherMap[keyID]
                        tempData = pitcherMap[keyID]
                    else:
                        yearsMissing.append(year)
                for yr in yearsMissing:
                    player_2010to2015[yr] = tempData
            else: # batter
                tempData = {}
                yearsMissing = []
                for year in range(2010, 2015 + 1):
                    keyID = str(pid) + "_" + str(year)
                    if keyID in batterMap:
                        player_2010to2015[str(year)] = batterMap[keyID]
                        tempData = batterMap[keyID]
                    else:
                        yearsMissing.append(year)
                if normalize:
                    for yr in yearsMissing:
                        player_2010to2015[str(yr)] = tempData
            newList = []
            print "Pre-mod",  player_2010to2015
            if raw:
                for i, (d, vals) in enumerate(player_2010to2015.iteritems()):
                    if i == 0:
                        newList = map(lambda x: float(x) if x != '' else 0, list(vals.values()))
                    else:
                        newList = map(lambda x: float(x) if x != '' else 0, list(vals.values())) + newList
                    print newList
                    player_2010to2015 = newList
        return info2016, playerPitchFxData, player_2010to2015
    
    print "Demonstrating an example using Mike Trout"
    trout2016, troutPitchFX2015, trout2010to2015 = getPlayerInformation("Mike Trout")
    print trout2016
    print '\n\n'
    print troutPitchFX2015
    print '\n\n'
    print trout2010to2015
    print '\n\n'
    # print batterMap[]


    # Prints the names of the statistical categories that are tracked by the database
    def printStatCategories():
        print "2016 statistics (Y) include: "
        print trout2016.keys()
        print
        print "peripheral statistics are available from 2015 and include: "
        print troutPitchFX2015.keys()
        print
        print "2010 to 2015 statistics used for training include: "
        for yr in trout2010to2015.keys():
            print yr, " includes --> ", trout2010to2015[yr].keys()

    # Print all available statistical categories
    printStatCategories()



    # Create the X dataset for linear regression
    pitcherX = []
    pitcherY = []
    batterX = []
    batterY = []
    # Example of creating a dataset
    def createTrainSet():
        for player, val in batter_2015_pitchfx.iteritems():
            player2016, playerFX2015, player2010to2015 = getPlayerInformation(player, True, True)
            if player2016 and playerFX2015 and player2010to2015: # ignore values not present in all categories
                player2016 = map(lambda x: float(x) if x != '' else 0, list(player2016.values()))
                batterY.append(player2016)
                playerFX2015 = map(lambda x: float(x) if x != '' else 0, list(playerFX2015.values()))
                batterX.append(player2010to2015 + playerFX2015)
        for player, val in pitcher_2015_pitchfx.iteritems(): # ignore values not present in all categories
            player2016, playerFX2015, player2010to2015 = getPlayerInformation(player, True, True)
            if player2016 and playerFX2015 and player2010to2015:
                player2016 = map(lambda x: float(x) if x != '' else 0, list(player2016.values()))
                pitcherY.append(player2016)
                playerFX2015 = map(lambda x: float(x) if x != '' else 0, list(playerFX2015.values()))
                pitcherX.append(player2010to2015 + playerFX2015)
        # print pitcherX
    # To run linear regression / create a neural net, we need to:
    # Separately for pitchers and hitters
    # 1. join the different data sets into a smaller sample set
        # Y response variable will be bbref2016 data
        # X will be PitchFX data and 2010 to 2015 data

    # When a user inputs a name of a player, we generate our X
    # from our 2010-2015 data set and if we don't have pitchfx data,
    # we scrape their 2015 pitch fx data from fangraphs

    # createTrainSet()
    # regr = linear_model.LinearRegression()
    # regr.fit(batterX, batterY)
    # print regr.coef_
    #     regr.predict(years)
    #     coeffs = regr.coef_
    #     intercept = regr.intercept_
    #     result = intercept
    #     lastYearData = years[-1]

    # INSTEAD JUST HAVE THE USER INPUT THEIR OWN PREFERENCES AND WE'LL JUST PULL VALUES FROM OUR DATASETS


if __name__ == '__main__':
    main()
