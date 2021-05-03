import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

# The coeffieient ranges from -1 to 1   ... .

forwards_who_can_score_df = pd.read_csv("forwards_who_can_score_df.csv", header=0)

finishing_df = forwards_who_can_score_df[['rank', 'Finishing']]

slope, intercept, r_value, p_value, std_err = stats.linregress(finishing_df['rank'], finishing_df['Finishing'])

sns.regplot(finishing_df['rank'], finishing_df['Finishing']).\
    set_title("Country's FIFA Ranking vs its Forwards Finishing Ability")
plt.xlabel('FIFA Ranking')
plt.ylabel('Mean Finishing Ability for Forwards (out of 20)')

print('The linear coefficient is', r_value)

