import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# The coeffieient ranges from -1 to 1   ... .

defenders_who_can_head_df = pd.read_csv("defenders_who_can_head_df.csv", header=0)
defenders_who_can_tackle_df = pd.read_csv("defenders_who_can_tackle_df.csv", header=0)
midfielders_who_can_pass_df = pd.read_csv("midfielders_who_can_pass_df.csv", header=0)
forwards_who_can_score_df = pd.read_csv("forwards_who_can_score_df.csv", header=0)

defenders_who_can_head_df = defenders_who_can_head_df.drop(['Simple Position'], axis=1)
defenders_who_can_tackle_df = defenders_who_can_tackle_df.drop(['Simple Position'], axis=1)
midfielders_who_can_pass_df = midfielders_who_can_pass_df.drop(['Simple Position'], axis=1)
forwards_who_can_score_df = forwards_who_can_score_df.drop(['Simple Position'], axis=1)

all_of_the_above_df = defenders_who_can_head_df.merge(defenders_who_can_tackle_df, how='left')
all_of_the_above_df = all_of_the_above_df.merge(midfielders_who_can_pass_df, how='left')
all_of_the_above_df = all_of_the_above_df.merge(forwards_who_can_score_df, how='left')

all_of_the_above_df['all_4_abilities'] = all_of_the_above_df[['Heading', 'Tackling', 'Passing', 'Finishing']].mean(axis=1)

a_bit_of_everything_df = all_of_the_above_df [['rank', 'all_4_abilities']]

slope, intercept, r_value, p_value, std_err = stats.linregress(a_bit_of_everything_df['rank'],
                                                               a_bit_of_everything_df['all_4_abilities'])

sns.regplot(a_bit_of_everything_df['rank'], a_bit_of_everything_df['all_4_abilities']).\
    set_title("Mean Rating for Tackling and Heading (Defenders), Passing (Midfielders) and Finishing (Forwards)")
plt.xlabel('FIFA Ranking')
plt.ylabel('Heading, Tackling, Passing and Finishing Mean Score')

print('The linear coefficient is', r_value)

