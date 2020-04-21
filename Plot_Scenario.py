import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import os

ROOT = os.getcwd()
filePath = os.path.abspath(os.path.join(ROOT, ".."))

actor_location = pd.read_csv(os.path.join(filePath, "Desktop\\Collections.csv"))
tgt_location = pd.read_csv(os.path.join(filePath, "Desktop\\Target_deck.csv"))

totalActorsCaught = len(actor_location.iloc[:,0].drop_duplicates())
totalTargets = len(tgt_location.iloc[:,0].drop_duplicates())

tgt_location['height'] = tgt_location['top'] - tgt_location['bottom']
tgt_location['width'] = tgt_location['right'] - tgt_location['left']
tgt_location = pd.DataFrame(tgt_location)

fig, ax = plt.subplots()
current_axes = plt.gca()

for index, target in tgt_location.iterrows():
    rect = patches.Rectangle((int(target['left']), int(target['bottom'])), int(target['width']),
                             int(target['height']), linewidth=1, edgecolor='r', facecolor='none')
    current_axes.add_patch(rect)


ax.scatter(actor_location['left'], actor_location['bottom'], s=1, color='black')
plt.title('Target Deck with Caught Actors')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.annotate("%s Targets Caught \n%s Targets in deck" % (totalActorsCaught, totalTargets), xy=(0.8, 1.01),
             xycoords='axes fraction', fontsize=10)
# plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()
