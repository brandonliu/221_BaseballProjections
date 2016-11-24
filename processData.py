import pandas as pd
from sqlalchemy import create_engine
import sqlite3

battingFile = '/Users/BrandonLiu/Documents/Stanford/Junior/CS221/final_project/221_BaseballProjections/lahman_csv_2015/core/Batting.csv'
idFile = '/Users/BrandonLiu/Documents/Stanford/Junior/CS221/final_project/221_BaseballProjections/lahman_csv_2015/core/Master.csv'
pitchingFile = '/Users/BrandonLiu/Documents/Stanford/Junior/CS221/final_project/221_BaseballProjections/lahman_csv_2015/core/Pitching.csv'

# create engine and database for batting file
bat_engine = create_engine('sqlite:///batting_table.db')
battingDF = pd.read_csv(battingFile)
battingDF.to_sql('batting_data', con=bat_engine, if_exists='append', index=False)
batTestQuery = pd.read_sql_query('SELECT * FROM batting_data LIMIT 3', bat_engine)
print "Batting test query:", batTestQuery
bat_data_10_15 = pd.read_sql_query('SELECT * FROM batting_data WHERE yearID >= 2010 and yearID <= 2015', bat_engine)
print len(bat_data_10_15)

# create engine and database for pitching file
pitch_engine = create_engine('sqlite:///pitching_table.db')
pitchingDF = pd.read_csv(pitchingFile)
pitchingDF.to_sql('pitching_data', con=pitch_engine, if_exists='append', index=False)
pitchTestQuery = pd.read_sql_query('SELECT * FROM pitching_data LIMIT 3', pitch_engine)
print "Pitching data test query:", pitchTestQuery

# create engine and database for id file
masterID_engine = create_engine('sqlite:///id_table.db')
idDF = pd.read_csv(idFile)
idDF.to_sql('id_data', con=masterID_engine, if_exists='append', index=False)
idTestQuery = pd.read_sql_query('SELECT * FROM id_data LIMIT 3', masterID_engine)
print "ID data test query:", idTestQuery

# create the database
#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
# commit
# then next time just load it

# alternative approach --> manually create database and store a .db file in github
# use connect instead?



# find average of statistics for past year or so