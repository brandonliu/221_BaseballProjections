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
import matplotlib.pyplot as plt
import sys
import collections

if __name__ == '__main__':

    # run on csvfile: 'lahman_csv_2015/core/Batting.csv'
    # run on csvfile: 'lahman_csv_2015/core/Master.csv'

    battingFile = 'lahman_csv_2015/core/Batting.csv'
    masterFile = 'lahman_csv_2015/core/Master.csv'
    pitchingFile = 'lahman_csv_2015/core/Pitching.csv'
    bat_2016File = 'ESPN_batters_2016.csv'
    pitch_2016File = 'ESPN_pitchers_2016.csv'
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
                if playerName not in idNamePairs:
                    idNamePairs[playerName] = [(pid, row['debut'])]
                else:
                    idNamePairs[playerName].append((pid, row['debut']))

    
    # ii. Data source: espn_2016
    def generate2016Data(filename2016, newMap):
        with open(filename2016) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print row
                name = row['Name']
                if name in newMap:
                    if row['Tm'] != 'TOT':
                        continue
                newMap[name] = row



    # iii. Data source: pitchfx
    def generatePitchFXData(filenamePitchfx, newMap):
        with open(filenamePitchfx) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                newMap[name] = row


    print "Generate data frame from ESPN 2016 data...."
    espn_2016_batters = {}
    espn_2016_pitchers = {}
    generate2016Data(bat_2016File, espn_2016_batters)
    generate2016Data(pitch_2016File, espn_2016_pitchers)
    # print espn_2016_pitchers

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
        # print val, idMap[key]
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
    print dupPlayers


    # Create the methods to access player data when given a player name

    # Input: A string of a player's name (e.g. Mike Trout)
    # If there are duplicates found, then it will prompt the user for which
    # player they are interested in.
    def getPlayerInformation(playerName):
        # Get 2016 information
        info2016 = None
        batter = True
        playerCurrent = False
        if playerName in espn_2016_batters:
            info2016 = espn_2016_batters[playerName]
            playerCurrent = True
        elif playerName in espn_2016_pitchers:
            batter = False
            info2016 = espn_2016_pitchers[playerName]
            playerCurrent = True
        if not playerCurrent:
            print "Player no longer active."
            return None
        playerPitchFxData = None
        if batter:
            playerPitchFxData = batter_2015_pitchfx[playerName]
        else:
            playerPitchFxData = pitcher_2015_pitchfx[playerName]
        player_2010to2015 = {}
        playerIDInfo = idNamePairs[playerName][0] # Just takes the first player it finds
        pid = playerIDInfo[0]
        if batter:
            for i in range(2010, 2015 + 1):
                keyID = str(pid) + "_" + str(i)
                print keyID
                # print batterMap
                if keyID in batterMap:
                    player_2010to2015[str(i)] = batterMap[keyID]
        else: # pitcher
            for i in range(2010, 2015 + 1):
                keyID = str(pid) + "_" + str(i)
                if keyID in batterMap:
                    player_2010to2015[str(i)] = pitcherMap[keyID]

        return info2016, playerPitchFxData, player_2010to2015
        
    trout2016, troutPitchFX2015, trout2010to2015 = getPlayerInformation("Mike Trout")
    print trout2016
    print '\n\n'
    print troutPitchFX2015
    print '\n\n'
    print trout2010to2015
    print '\n\n'