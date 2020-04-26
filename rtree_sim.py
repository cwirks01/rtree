import os
import pandas as pd
from rtree import index
import random
import time

random.seed(0)  # Need random seed to perform test
NUM_TARGETS = 1000
NUM_ACTORS = 10000

ROOT = os.getcwd()
outputFile = os.path.abspath(os.path.join(ROOT, ".."))

#  Creating a file that will keep track of the statistics of the run
timeEvalFile_path = os.path.join(outputFile, 'Desktop\\rtree_Stats.csv')
if os.path.isfile(timeEvalFile_path):
    timeEvalFile = pd.read_csv(timeEvalFile_path)
else:
    timeEvalFile = pd.DataFrame([], columns=['NumOfTargets', 'NumOfActors', 'TimeToProcessActors (s)',
                                             'TimeToProcessScenario (s)'], index=[0])


def _build_rtree(locations, rtreeIdx):
    """ build environment of scenario using the bounded area in generate_actors """
    # Will initiate with the largest bounded area
    for location in locations['coord']:
        if location[1].startswith("Actor"):
            rtreeIdx.insert(4444, location[0], location[1])
        else:  # id 5555 will be the box coordinates
            rtreeIdx.insert(5555, location[0], location[1])
    return


def generate_actors(num_of_actors=NUM_ACTORS):
    """
    Actors are randomly generated throughout a grid of a 1000 x 1000
    Inserting a point into a rtree left == right and bottom == top

    :param num_of_actors:
    :return:
    """
    actors = dict()
    actors_loc = []
    for i in range(num_of_actors):
        randomPoint_x, randomPoint_y = (random.randint(0, 1000), random.randint(0, 1000))
        loc = ((randomPoint_x, randomPoint_y, randomPoint_x, randomPoint_y), "Actor: " + str(i))
        actors_loc.append(loc)
        actors['coord'] = actors_loc
    return actors


def actors_in_collect(targetDeck, rtreeIdx):
    """
    This will be the method to find if the actors are in our target deck
    This will have a true and false statement where if true will return the actors id and coordinates as well as which
    box, or "target deck", they are in
    """
    all_collects = []
    for i, target in enumerate(targetDeck):
        hits = list(rtreeIdx.intersection(target[0], objects=True))
        collected = [(target[1], item.object, tuple(item.bbox)) for item in hits]
        all_collects.append(collected)

    return all_collects


def build_tgt_deck(num_targets=NUM_TARGETS):
    """
    build_tgt_deck generate randomly placed rectangles with varying sides on a grid of a 1000
    X and Y values less than zero will not be appended to the list of targets
    :return:
    """
    t_new = dict()
    tgt_deck = []
    for i in range(num_targets):
        randomPoint_x, randomPoint_y = (random.randint(10, 1000), random.randint(10, 1000))
        width, height = (random.randint(1, 5) * 2, random.randint(1, 5) * 2)
        x_min, x_max = (randomPoint_x - width, randomPoint_x + width)
        y_min, y_max = (randomPoint_y - height, randomPoint_y + height)
        rect = ((x_min, y_min, x_max, y_max), "Location:" + str(i))

        tgt_deck.append(rect)
        t_new['coord'] = tgt_deck

    return t_new


# Run script here
if __name__ == '__main__':
    p = index.Property()
    idx = index.Index(properties=p)
    actors_gen = generate_actors()
    actorScenario = pd.DataFrame(actors_gen['coord'], columns=['Coordinates', 'ActorsName'])
    tgt_location = build_tgt_deck()
    locs = tgt_location['coord']
    _build_rtree(actors_gen, idx)
    # _build_rtree(tgt_location, idx) # Testing to evaluate targets separately from R-tree

    # Starting time after scenario is built
    start = time.perf_counter()

    actors_caught = actors_in_collect(locs, idx)

    # if multiple actors were caught in the same targeted box this will create another column
    actorsInTargets = len(actors_caught)
    timeProcessActors = time.perf_counter() - start
    print("time to process %s actors and %s locations: %.03f s" % (NUM_ACTORS, actorsInTargets, (timeProcessActors)))
    actors_caught = pd.DataFrame(actors_caught)
    colNames = []
    for i in range(len(actors_caught.columns)):
        colNames.append('Collections%s' % (i + 1))
    actors_caught.columns = colNames
    actors_caught = actors_caught.dropna(subset=['Collections1'])
    actors_caught = actors_caught.stack().reset_index(drop=True)
    actors_caught = pd.DataFrame(actors_caught.tolist(), columns=['Location', 'Actors', 'Coordinates'])

    locs = pd.DataFrame(tgt_location['coord'], columns=['Coordinates', 'TargetLocation'])
    new_col_list = ['left', 'bottom', 'right', 'top']
    for n, col in enumerate(new_col_list):
        actors_caught[col] = actors_caught['Coordinates'].apply(lambda location: location[n])
        locs[col] = locs['Coordinates'].apply(lambda location: location[n])
    locs = locs.drop('Coordinates', axis=1)
    actors_caught = actors_caught.drop('Coordinates', axis=1)

    actors_caught.to_csv(os.path.join(outputFile, "Desktop\\Collections.csv"), index=False)
    locs.to_csv(os.path.join(outputFile, "Desktop\\Target_deck.csv"), index=False)
    actorScenario.to_csv(os.path.join(outputFile, "Desktop\\Actors_location.csv"), index=False)

    # Python time.clock is deprecated, but process_time and perf_counter does not send back ns
    entireEventTime = time.perf_counter() - start
    print("time to process whole event: %.03f s" % (entireEventTime))
    timeEvalFile_cols = timeEvalFile.columns
    timeEvalFile = timeEvalFile.append({timeEvalFile_cols[0]: NUM_TARGETS, timeEvalFile_cols[1]: NUM_ACTORS,
                                        timeEvalFile_cols[2]: timeProcessActors,
                                        timeEvalFile_cols[3]: entireEventTime}, True).dropna().reset_index(drop=True)
    timeEvalFile.to_csv(timeEvalFile_path, index=False)
