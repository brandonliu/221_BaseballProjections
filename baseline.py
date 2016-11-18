import csv
import sys
import math


if __name__ == '__main__':

    # run on csvfile: 'lahman_csv_2015/core/Batting.csv'
    # run on csvfile: 'lahman_csv_2015/core/Master.csv'

    battingFile = 'lahman_csv_2015/core/Batting.csv'
    masterFile = 'lahman_csv_2015/core/Master.csv'
    pitchingFile = 'lahman_csv_2015/core/Pitching.csv'

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

    def generatePlayerMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_year_key = str(row['playerID']) + "_" + str(row['yearID'])
                map[id_year_key] = row

    newBatterMap = {}
    def generateBatterMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if int(row['yearID']) < 2010 or int(row['yearID']) > 2014:
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


    newPitcherMap = {}
    def generatePitcherMap(filename, map):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row['yearID']) < 2010 and int(row['yearID']) > 2014:
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


    # function averages values from 2010 to 2014 for hitters from an
    # associated map with values containing aggregated data on those years
    avg_hitter_map = {}
    def averageBattingValues_baseline(map):
        for pid, stats in map.iteritems():
            years = map[pid]['numYears']
            newMap = {}
            newMap['HR'] = float(map[pid]['HR'])/years
            newMap['G'] = float(map[pid]['G'])/years
            newMap['R'] = float(map[pid]['R'])/years
            newMap['AB'] = float(map[pid]['AB'])/years
            newMap['H'] = float(map[pid]['H'])/years
            newMap['RBI'] = float(map[pid]['RBI'])/years
            newMap['SB'] = float(map[pid]['SB'])/years
            # for key, val in map[playerID]:
            #     print map[playerID]
            #     print key
            #     newMap[key] = float(val)/years
            avg_hitter_map[pid] = newMap
        # for key, val in avg_hitter_map.iteritems():
        #     print key, val
        # for pid, stats in avg_hitter_map.iteritems():
        #     print pid, stats
        print "Nelson Cruz", avg_hitter_map['cruzne02']

    avg_pitcher_map = {}
    def averagePitchingValues_baseline(map):
        for pid, stats in map.iteritems():
            years = map[pid]['numYears']
            newMap = {}
            newMap['GS'] = float(map[pid]['GS'])/years
            newMap['BB'] = float(map[pid]['BB'])/years
            newMap['W'] = float(map[pid]['W'])/years
            newMap['ER'] = float(map[pid]['ER'])/years
            newMap['H'] = float(map[pid]['H'])/years
            newMap['L'] = float(map[pid]['L'])/years
            newMap['IPouts'] = float(map[pid]['IPouts'])/years
            # for key, val in map[playerID]:
            #     print map[playerID]
            #     print key
            #     newMap[key] = float(val)/years
            avg_pitcher_map[pid] = newMap
        # for key, val in avg_pitcher_map.iteritems():
        #     print key, val
        print "Clayton Kershaw", avg_pitcher_map['kershcl01']


    def checkAccuracyPitching():
        pass

    hittingAccuracy = {}
    def checkAccuracyHitting():
        for pid, stats in avg_hitter_map.iteritems():
            accuracyVec = {}
            key2015 = str(pid) + "_" + '2015'
            if batterMap.get(key2015, 0) == 0:
                continue
            for key, val in avg_hitter_map[pid].iteritems():
                # print key, val
                comparisonVal = float(batterMap[key2015][key])
                if comparisonVal == 0:
                    comparisonVal = 1
                accuracy = abs(float(val - comparisonVal)/comparisonVal)
                accuracyVec[key] = accuracy
            hittingAccuracy[pid] = accuracyVec
        # for key, val in hittingAccuracy.iteritems():
        #     print key, val
        print newBatterMap['troutmi01']

        print "Trout prediction 2015", avg_hitter_map['troutmi01']
        print "Trout actual 2015", batterMap['troutmi01_2015']
        print "Trout error 2015", hittingAccuracy['troutmi01']


        totalABs = 0
        totalAverages = {'HR':0, 'G':0, 'R':0, 'AB':0, 'H':0, 'RBI':0, 'SB':0}
        for pid, val in hittingAccuracy.iteritems():
            key_2015 = str(pid) + "_" + '2015'
            print key_2015, batterMap[key_2015]
            print pid, avg_hitter_map[pid]
            currABs = int(batterMap[key_2015]['AB'])
            currHRs = int(batterMap[key_2015]['HR'])
            if currABs < 50 and currHRs < 2:
                continue
            for key, val in hittingAccuracy[pid].iteritems():
                totalAverages[key] += val #* float(batterMap[key_2015]['AB'])
                # totalABs += float(batterMap[key_2015]['AB'])

        for keyAcc, valAcc in totalAverages.iteritems():
            # print totalAverages[keyAcc]
            totalAverages[keyAcc] = float(valAcc) / len(hittingAccuracy) #/ totalABs

        print totalAverages


    def generateIDTable(map = idMap):
        with open(masterFile) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                map[str(row['playerID'])] = row


    generatePlayerMap(battingFile, batterMap)
    generatePlayerMap(pitchingFile, pitcherMap)
    generateIDTable()

    # create averaged values to compare with
    generateBatterMap(battingFile, newBatterMap)
    generatePitcherMap(pitchingFile, newPitcherMap)
    averageBattingValues_baseline(newBatterMap)
    averagePitchingValues_baseline(newPitcherMap)
    checkAccuracyHitting()



    # Test cases -------
    # print "Hank Aaron test - 1957", batterMap['aaronha01_1957']
    # print "Clayton Kershaw test - 2013", pitcherMap['kershcl01_2013']
    # print "Hank Aaron id test", idMap['aaronha01']


    