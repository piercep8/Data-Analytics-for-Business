import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# The coeffieient ranges from -1 to 1   ... .

midfielders_who_can_pass_df = pd.read_csv("midfielders_who_can_pass_df.csv", header=0)

passing_df = midfielders_who_can_pass_df[['rank', 'Passing']]

slope, intercept, r_value, p_value, std_err = stats.linregress(passing_df['rank'], passing_df['Passing'])

sns.regplot(passing_df['rank'], passing_df['Passing']).\
    set_title("Country's FIFA Ranking vs its Midfielders Passing Ability")
plt.xlabel('FIFA Ranking')
plt.ylabel('Mean Passing Ability for Midfielders (out of 20)')

print('The linear coefficient is', r_value)

