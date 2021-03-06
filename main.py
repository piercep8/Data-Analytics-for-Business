#
# Program 1 Clean and Convert Raw Data
# ------------------------------------
# In this program we'll do the following...
#    * Use the FIFA rankings to select the top 50 countries in the world at at April 2021.
#    * Create 23 man squads for each of those countries based on the "Scout Rating" score
#      from the Football Manager database.
#
# Inputs
# ------
# 1) Football Manager March 20 Full Attribute Database.csv : Attributes and statistics for 150,000 players as at
#                                                            March 2020.
# 2) fifa_ranking-2021-04-07.csv                           : An historical list of each nation's FIFA ranking up to
#                                                            April 2021.
# Outputs
# -------
# 1) squad_list_df._csv        : The top 50 teams and 23 man squads for each of them.
# 2) outfield_players_df.csv   : A version of the squad list data frame without goalkeepers.
# 3) stamina_df.csv            : Mean stamina rating for outfield players this is used in two of the graph building
#                                programs so it's produced once here to save on duplication.
# 4) work_rate_df.csv          : As with stamina this is used in two places. It gives the mean work rate rating for
#                                all players.
#
import numpy as np
import pandas as pd

# Simplified Position Dictionary - to be used to convert the various midfield positions a generic midfield role
simple_position_dict = {'A': '4: FWD', 'AM': '3: MID', 'G': '1: GK', 'D': '2: DEF', 'DM': '3: MID', 'M': '3: MID', 'W': '3: MID'}

fifa_country_list = ['Netherlands', 'USA', 'IR Iran', 'Korea Republic', 'Republic of Ireland',
                     'Northern Ireland', 'Bosnia and Herzegovina', 'Côte dIvoire', 'Congo DR', 'Cabo Verde',
                     'United Arab Emirates', 'China PR', 'Kyrgyz Republic', 'Trinidad and Tobago',
                     'Korea DPR', 'Central African Republic', 'Antigua and Barbuda', 'St. Kitts and Nevis',
                     'Suriname', 'Swaziland', 'St. Vincent / Grenadines', 'St. Lucia', 'Brunei Darussalam',
                     'Timor-Leste', 'Turks and Caicos Islands', 'US Virgin Islands', 'British Virgin Islands']
master_country_list = ['Holland', 'U.S.A.', 'Iran', 'South Korea', 'Ireland', 'N.Ireland', 'Bosnia', 'Ivory Coast',
                       'Congo', 'Cape Verde', 'U.A.E.', 'China', 'Kyrgyzstan', 'Trinidad & Tobago', 'North Korea',
                       'Central African Rep.', 'Antigua & Barbuda', 'St Kitts & Nevis', 'Surinam', 'eSwatini',
                       'St Vincent', 'St Lucia', 'Brunei', 'Timor', 'Turks and Caicos Is.', 'US Virgin Is.',
                       'British Virgin Is.']

#                           ----- Import and Format Current FIFA World Rankings File -----
fifa_rankings_db = pd.read_csv("fifa_ranking-2021-04-07.csv", header=0)
# Convert to a Data Frame
fifa_rankings_df = pd.DataFrame(fifa_rankings_db)
# Sort by Ranking Date (most recent first) and then world ranking (highest first)
fifa_rankings_df['rank_date'] = pd.to_datetime(fifa_rankings_df['rank_date'])
fifa_rankings_df = fifa_rankings_df.sort_values(['rank_date', 'rank'], ascending=[False, True])
fifa_rankings_df = fifa_rankings_df.rename(columns={'country_full': 'Nation'})

# Limit to only the most recent rank date
latest_rank_date = fifa_rankings_df['rank_date'].max()
fifa_rankings_df = fifa_rankings_df[fifa_rankings_df['rank_date'] == latest_rank_date]

# Create a list of just the countries, their ranking and short_name
fifa_countries_df = fifa_rankings_df[['Nation', 'rank', 'country_abrv']]

#                                 ------ Import and Format Player Data File -----
# Import CSV File and set the first row as the header. Store as a Pandas Data Frame
master_football_db = pd.read_csv("Football Manager March 20 Full Attribute Database.csv", header=0,
                                 encoding='ISO-8859-1')
master_football_df = pd.DataFrame(master_football_db)

# Split the Scout Rating Column into 2 columns and remove the % element to leave a score out 100
master_football_df[['Scout Rating', 'Best Position']] = master_football_df['Scout Rating'].str.split('%', 1,
                                                                                                     expand=True)

# Split the Nation column into two where players have a 2nd nationality
master_football_df[['Nation', '2nd Nation']] = master_football_df['Nation'].str.split('/', 1, expand=True)

# Remove tabs from the Best Position Column
master_football_df['Best Position'] = master_football_df['Best Position'].replace("\t", " ", regex=True)

# Remove leading spaces and brackets from the Best Position Column
master_football_df['Best Position'] = master_football_df['Best Position'].apply(lambda x: x.strip())
master_football_df['Best Position'] = master_football_df['Best Position'].map(lambda x: x.lstrip('(').rstrip(')'))

# Change Scout Rating from type Object to type Float
master_football_df['Scout Rating'] = pd.to_numeric(master_football_df['Scout Rating'])

# Remove tabs from the Player Name column
master_football_df['Name'] = master_football_df['Name'].replace("\t", " ", regex=True)

# Simplify the positions so Wingers, Defensive Midfielders and Attacking Midfielders are all grouped as Midfielders
master_football_df['Simple Position'] = master_football_df['Best Position'].map(simple_position_dict)

# Split the Simple Position column to produce a position order column. So "1: GK" becomes "1" and "GK"
master_football_df[['position order', 'Simple Position']] = master_football_df['Simple Position'].str.split(':', 1, expand=True)
master_football_df['Simple Position'] = master_football_df['Simple Position'].apply(lambda x: x.strip())

# Change the names of Nations in the Master Football Data Frame to match those on the FIFA World Rankings Data Frame
i = len(master_country_list)
for country in range(i):
    master_football_df['Nation'] = master_football_df['Nation'].replace(master_country_list[country],
                                                                        fifa_country_list[country])

# Add the FIFA rankings column onto the Master Football Data Frame
master_football_df = master_football_df.merge(fifa_countries_df, how='left')

# Sort the dataframe into Nation (A-Z), Simple Position (A-Z) and Scout Rating (Highest to Lowest)
master_football_df = master_football_df.sort_values(['rank', 'Nation', 'position order', 'Scout Rating'],
                                                    ascending=[True, True, True, False])

# Produce a subset of the Master Football DF based on player position
goalkeepers_df = master_football_df[(master_football_df['Simple Position'] == 'GK')]
defenders_df = master_football_df[(master_football_df['Simple Position'] == 'DEF')]
midfielders_df = master_football_df[(master_football_df['Simple Position'] == 'MID')]
attackers_df = master_football_df[(master_football_df['Simple Position'] == 'FWD')]

# Create a new dataframe to hold my squad lists for the top 50 teams based on current FIFA World Rankings
squad_list_df = pd.DataFrame()
ave_rating_df = pd.DataFrame([['rank', 'country_abrv','position order', 'Simple Position', 'Scout Rating', 'Ave Rating']])

# Loop through our position based dataframes and for each team in the FIFA top 50, produce a squad based on
for team in range(51):
    temp_goalkeepers_df = goalkeepers_df[(goalkeepers_df['rank'] == team)]
    temp_goalkeepers_df = temp_goalkeepers_df.head(3)
    squad_list_df = squad_list_df.append(temp_goalkeepers_df)
    temp_defenders_df = defenders_df[(defenders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_defenders_df.head(8))
    temp_midfielders_df = midfielders_df[(midfielders_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_midfielders_df.head(7))
    temp_attackers_df = attackers_df[(attackers_df['rank'] == team)]
    squad_list_df = squad_list_df.append(temp_attackers_df.head(5))
#
# This data frame is the basis of all the dataframes that will be used to produce our graphs
squad_list_df = squad_list_df.sort_values(['rank', 'country_abrv', 'position order', 'Scout Rating'],
                                          ascending=[True, True, True, False])
#
# Datasets for Graph Plotting
#
# Create files that show the mean value for each position (GK, DEF, MID and FWD) for selected squads based on
# FIFA world ranking
# Average Rating for Each Squad for Each Position
ave_rating_df = squad_list_df.groupby(['rank', 'country_abrv', 'position order', 'Simple Position'],
                                      as_index=False)['Scout Rating'].mean()
graph_ave_rating_df = ave_rating_df[['rank', 'country_abrv', 'Simple Position', 'Scout Rating']]
# Merge Country and Position together to give "BEL GK" or "ENG MID"
graph_ave_rating_df['country_pos'] = graph_ave_rating_df['country_abrv'].map(str)+' ' + \
                                     graph_ave_rating_df['Simple Position']
# Create files to display on graphs based on ranking
ave_rating_1_to_5_df = graph_ave_rating_df[(graph_ave_rating_df["rank"] <= 5)]
ave_rating_6_to_10_df = graph_ave_rating_df[graph_ave_rating_df["rank"].between(6, 10)]
ave_rating_40_to_45_df = graph_ave_rating_df[graph_ave_rating_df["rank"].between(40, 45)]
ave_rating_46_to_50_df = graph_ave_rating_df[graph_ave_rating_df["rank"].between(46, 50)]

# Johan Cryuff Desired Skills and Attributes
# as a lot of these stats aren't applicable to goalkeepers they've been ruled out for this set of averages
outfield_players_df = squad_list_df[(squad_list_df['Simple Position'] != 'GK')]
anticipation_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Anticipation'].mean()
decisions_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Decisions'].mean()
off_the_ball_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Off The Ball'].mean()
positioning_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Positioning'].mean()
nat_fitness_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Nat Fitness'].mean()
stamina_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Stamina'].mean()
work_rate_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Work Rate'].mean()

# Alex Ferguson Desired Skills and Attributes
ambition_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Ambition'].mean()
determination_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Determination'].mean()
pressure_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Pressure'].mean()
professionalism_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Professionalism'].mean()
temperament_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Temperament'].mean()

# Kevin Keegan Desired Skills and Attributes
# Some of these stats aren't applicable to defenders or goalkeepers so they've been ruled out when needed
attack_minded_players_df = outfield_players_df[(outfield_players_df['Simple Position'] != 'DEF')]
sportsmanship_df = squad_list_df.groupby(['rank', 'country_abrv'], as_index=False)['Sportsmanship'].mean()
technique_df = outfield_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Technique'].mean()
creativity_df = attack_minded_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Creativity'].mean()
flair_df = attack_minded_players_df.groupby(['rank', 'country_abrv'], as_index=False)['Flair'].mean()

# Create csv files for our graph data
squad_list_df.to_csv('squad_list.csv', header=True, encoding='ISO-8859-1', index=False)
outfield_players_df.to_csv('outfield_players_df.csv', header=True, encoding='ISO-8859-1', index=False)
stamina_df.to_csv('stamina_df.csv', header=True, encoding='ISO-8859-1', index=False)
work_rate_df.to_csv('work_rate_df.csv', header=True, encoding='ISO-8859-1', index=False)
