import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# The coeffieient ranges from -1 to 1   ... .

defenders_who_can_head_df = pd.read_csv("defenders_who_can_head_df.csv", header=0)

heading_df = defenders_who_can_head_df[['rank', 'Heading']]

slope, intercept, r_value, p_value, std_err = stats.linregress(heading_df['rank'], heading_df['Heading'])

sns.regplot(heading_df['rank'], heading_df['Heading']).\
    set_title("Country's FIFA Ranking vs Its Defenders Heading Ability")
plt.xlabel('FIFA Ranking')
plt.ylabel('Mean Score for Defenders Heading Ability(max 20)')

print('The linear coefficient is', r_value)

