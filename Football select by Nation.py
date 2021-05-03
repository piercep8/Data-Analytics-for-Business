# Read the file

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl

# Import excel spreadsheet
football_db = pd.read_excel("Football Manager March 2020 Player Stats.xlsx", sheet_name="Main", header=0)



# Select players by nation
england_players = football_db.loc[football_db['Nation'] == 'England']

# Limit to first ten players
england_players_top_10 = england_players[:10]

print(england_players_top_10)