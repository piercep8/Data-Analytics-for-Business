# Read the file

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl

# Import excel spreadsheet
football_db = pd.read_excel("Football Manager March 2020 Player Stats.xlsx", sheet_name="Main", header=0)
# football_db = football_db.set_index(['Nation'])

in_scope_columns = ['Name', 'Nation', 'Club', 'Position', 'Age', 'Value', 'Scout Rating', 'Best Position']

# Select players by nation and limit columns returned
england_players = football_db.loc[football_db['Nation'] == 'England', in_scope_columns]
# england_players = england_players.set_index(['Scout Rating', 'Best Position'])

# Limit to top 50 players based on scout rating
england_players_top_50 = england_players.nlargest(50, ['Scout Rating'])

print(england_players_top_50)
