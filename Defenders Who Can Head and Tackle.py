import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# The coeffieient ranges from -1 to 1   ... .

defenders_who_can_tackle_df = pd.read_csv("defenders_who_can_tackle_df.csv", header=0)
defenders_who_can_head_df = pd.read_csv("defenders_who_can_head_df.csv", header=0)

defenders_who_can_head_and_tackle_df = defenders_who_can_head_df.merge(defenders_who_can_tackle_df, how='left')

defenders_who_can_head_and_tackle_df['head_and_tackle'] = defenders_who_can_head_and_tackle_df[['Heading', 'Tackling']]\
    .mean(axis=1)

heading_and_tackling_df = defenders_who_can_head_and_tackle_df[['rank', 'head_and_tackle']]

slope, intercept, r_value, p_value, std_err = stats.linregress(heading_and_tackling_df['rank'],
                                                               heading_and_tackling_df['head_and_tackle'])

sns.regplot(heading_and_tackling_df['rank'], heading_and_tackling_df['head_and_tackle']).\
    set_title("Defenders Who Can Head and Tackle")
plt.xlabel('FIFA Ranking')
plt.ylabel('Mean Score for Defenders Mean Heading & Tackling Ability(max 20)')

print('The linear coefficient is', r_value)

