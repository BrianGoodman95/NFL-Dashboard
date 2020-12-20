import time
import pandas as pd
import pathlib
from parsers import Game_Predictor
from parsers import Prediction_Analysis
from parsers.setup import Directory_setup, Dashboard_setup
setup = Directory_setup.Create_Directories()
project_path = setup.project_path
dir_path = pathlib.Path().absolute()
if 'home/BGoodman95/' in str(dir_path): #The Python Anywhere Dashboard
    proj_path_parts = project_path.split('NFL-Dashboard/N')
    project_path = f'{proj_path_parts[0]}N{proj_path_parts[1]}'
    print(project_path)
elif 'home/BGoodman95' in str(dir_path): #The Python Anywhere Dashboard
    proj_path_parts = project_path.split('NFL-Dashboard/N')
    print(dir_path)
    project_path = f'{dir_path}/NFL-Dashboard/data'
    print(project_path)

season, week = Dashboard_setup.This_Week()

'''
3 Modes to run the data parser with:
Weekly - Updates the current and last week predicitons/results only
Season - Updates every week in the current season
Historical - Updates every game ever
    To run Historical:
        -Need to enable the old WDVOA DF headers in Predition_Helper.Combine_DF
        -Need to enable a new naming convention to be made every week in Prediction_Helper.init (since Week 6 some seasons has byes)
        -Need to remove the margin==0 if condition in Prediction_Helper.Calculate_Data since historical ties are indistinguishable
        -Need to put the upper EGO-Spread Diff limit in (3.7) since no games_to_avoid
    Put everything back, then run the season parser to cleanup the latest season results from these changes
'''

Data = Game_Predictor.NFL_Game_Predictor(project_path, week, season, updateType='Week')
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
