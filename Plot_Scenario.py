import matplotlib.pyplot as plt
import pandas as pd

tgt_actor_location = pd.read_csv("C:\\Users\\cwirk\\Desktop\\Collections.csv")

# tgt_coord = tgt_actor_location.apply(lambda x: pd.Series(x['Coordinates']),
#                                      axis=1).stack().reset_index(level=1, drop=True)

new_col_list = ['Left', 'bottom', 'right', 'top']
for n,col in enumerate(new_col_list):
    tgt_actor_location[col] = tgt_actor_location['Coordinates'].apply(lambda location: location[n])

tgt_actor_location = tgt_actor_location.drop('Coordinates', axis=1)


