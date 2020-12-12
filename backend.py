import time
import pandas as pd
from parsers import Game_Predictor
from parsers import Prediction_Analysis
from parsers.setup import Directory_setup, Dashboard_setup
setup = Directory_setup.Create_Directories()
project_path = setup.project_path
proj_path_parts = project_path.split('NFL-Dashboard/N')
project_path = f'{proj_path_parts[0]}N{proj_path_parts[1]}'
print(project_path)

season, week = Dashboard_setup.This_Week()

#Want way to mark games with outside factors (injuries, weather, coaching changes, etc)
#Would manually indicate in a file the teams with a factor affecting and that game would automatically get a "Something Missing" designation
#Then we can remove the end caps on the EGO-Spread diff target since genuine extremes due to those factors are ignored
#In the def Calculate_Data(self, df): function, read in the games_to_avoid.csv and make dict of teams:reason for that week that don't have null values 
#For each team we normally go through:
    #Check if either team or opp is in the list of dict keys
    #If so, pick = 0 and spread target = "Avoid - {team/opp} {dict.reason}"
    #Else, do the regular thing

Data = Game_Predictor.NFL_Game_Predictor(project_path, week, season, updateType='Season')
Spread_Target_DF = Data.Spread_Targets
# print(f'Week {week} Evaluation:')
picks = Data.picks
# print(picks)
# print(Spread_Target_DF)

#Analyze Season Results
Results = Prediction_Analysis.Prediction_Analyzer(project_path, season)
Prediction_Stats = Results.Analyzed_Results
# print(Prediction_Stats)

#Add this Week to the Historical Database
database = f'{project_path}/All Game Data.csv' #Path To Master Data
database_df = pd.read_csv(database) #Read the Data
archived_database = database_df.loc[database_df['Season'] != season] #Exclude this season
this_season = pd.read_csv(f'{project_path}/raw data/{season}/Season Game Data.csv') #Read this seasons updated data
this_season = this_season.loc[this_season['Week'] != week] #Exclude this week
combined_df = pd.concat([archived_database, this_season]) #Combine old and this season data
combined_df.to_csv(database, index=False) #Save
