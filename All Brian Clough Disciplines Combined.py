import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# Read in Squad List Data Frame

squad_list_df = pd.read_csv("squad_list_df.csv", header=0, encoding='ISO-8859-1')

# Brian Clough desired Skills and Attributes
# ------------------------------------------
# 1) Defenders Who Can Head and Tackle
#    Produce the mean score for heading for all defenders per national team
#    Produce the mean score for tackling for  all defenders per national team
#    Combine the two to get a mean score for heading and tackling
defenders_who_can_head_df = squad_list_df[(squad_list_df['Simple Position'] == 'DEF')]
defenders_who_can_head_df = defenders_who_can_head_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                              as_index=False)['Heading'].mean()
defenders_who_can_tackle_df = squad_list_df[(squad_list_df['Simple Position'] == 'DEF')]
defenders_who_can_tackle_df = defenders_who_can_tackle_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                                  as_index=False)['Tackling'].mean()
defenders_who_can_head_and_tackle_df = defenders_who_can_head_df.merge(defenders_who_can_tackle_df, how='left')
defenders_who_can_head_and_tackle_df['head_and_tackle'] = defenders_who_can_head_and_tackle_df[['Heading', 'Tackling']]\
    .mean(axis=1)
#
# 2) Midfielders Who Can Pass
#    Produce the mean score for passing for all midfielders per national team
midfielders_who_can_pass_df = squad_list_df[(squad_list_df['Simple Position'] == 'MID')]
midfielders_who_can_pass_df = midfielders_who_can_pass_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                                  as_index=False)['Passing'].mean()
#
# Forwards Who Can Score
# Produce the mean score for sticking the ball in the net for all forwards per national team
forwards_who_can_score_df = squad_list_df[(squad_list_df['Simple Position'] == 'FWD')]
forwards_who_can_score_df = forwards_who_can_score_df.groupby(['rank', 'country_abrv', 'Simple Position'],
                                                              as_index=False)['Finishing'].mean()

defenders_who_can_head_df = defenders_who_can_head_df.drop(['Simple Position'], axis=1)
defenders_who_can_tackle_df = defenders_who_can_tackle_df.drop(['Simple Position'], axis=1)
midfielders_who_can_pass_df = midfielders_who_can_pass_df.drop(['Simple Position'], axis=1)
forwards_who_can_score_df = forwards_who_can_score_df.drop(['Simple Position'], axis=1)

# Combine all the attributes and produce a mean score for everything
all_of_the_above_df = defenders_who_can_head_df.merge(defenders_who_can_tackle_df, how='left')
all_of_the_above_df = all_of_the_above_df.merge(midfielders_who_can_pass_df, how='left')
all_of_the_above_df = all_of_the_above_df.merge(forwards_who_can_score_df, how='left')

all_of_the_above_df['all_4_abilities'] = all_of_the_above_df[['Heading', 'Tackling', 'Passing', 'Finishing']].mean(axis=1)

brian_clough_attributes_df = all_of_the_above_df [['rank', 'all_4_abilities']]

brian_clough_attributes_df.to_csv('brian_clough_attributes_df.csv', header=True, encoding='ISO-8859-1', index=False)

slope, intercept, r_value, p_value, std_err = stats.linregress(brian_clough_attributes_df['rank'],
                                                               brian_clough_attributes_df['all_4_abilities'])

sns.regplot(brian_clough_attributes_df['rank'], brian_clough_attributes_df['all_4_abilities']).\
    set_title("Mean Rating for Tackling and Heading (Defenders), Passing (Midfielders) and Finishing (Forwards)")
plt.xlabel('FIFA Ranking')
plt.ylabel('Heading, Tackling, Passing and Finishing Mean Score')

print('The linear coefficient is', r_value)

