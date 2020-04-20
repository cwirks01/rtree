import rtree as rt
import os
import pandas as pd
import numpy as np
from rtree import index
from rtree.index import Rtree
import random
import time

randomSeed = 0  # Need random seed to perform test
num_targets = 1000
num_actors = 10000

ROOT = os.getcwd()
outputFile = os.path.abspath(os.path.join(ROOT, ".."))


def _build_rtree(locations):
    """ build environment of scenario using the bounded area in generate_actors """
    # Will initiate with the largest bounded area
    for location in locations['coord']:
        if location[1].startswith("Actor"):
            idx.insert(4444, location[0], location[1])
        else:  # id 5555 will be the box coordinates
            idx.insert(5555, location[0], location[1])
    return


def generate_actors(num_of_actors):
    """
    Actors are randomly generated throughout a grid of a 1000 x 1000
    Inserting a point into a rtree left == right and bottom == top

    :param num_of_actors:
    :return:
    """
    actors = dict()
    actors_loc = []
    random.seed(randomSeed)
    for i in range(num_of_actors):
        randomPoint_x, randomPoint_y = (random.randint(0, 1000), random.randint(0, 1000))
        loc = tuple([(randomPoint_x, randomPoint_y, randomPoint_x, randomPoint_y), "Actor: " + str(i)])
        if not (randomPoint_x < 0) or (randomPoint_y < 0):
            actors_loc.append(loc)
        else:
            pass
        actors['coord'] = actors_loc
    return actors


def actors_in_collect(actors, targetDeck):
    """
    This will be the method to find if the actors are in our target deck
    This will have a true and false statement where if true will return the actors id and coordinates as well as which
    box, or "target deck", they are in
    """
    all_collects = []
    for i, target in targetDeck.iterrows():
        hits = list(idx.intersection(target['Coordinates'], objects=True))
        collected = [(target[1], item.object, tuple(item.bbox)) for item in hits]
        all_collects.append(collected)
    #
    # for actor in actors['coord']:
    #     hits = list(idx.intersection(actor[0], objects=True))
    #     collected = [(actor[1], item.object, tuple(item.bbox)) for item in hits if item.id == 5555]
    #     all_collects.append(collected)
    return all_collects


def build_tgt_deck():
    """
    build_tgt_deck generate randomly placed rectangles with varying sides on a grid of a 1000
    X and Y values less than zero will not be appended to the list of targets
    :return:
    """
    t_new = dict()
    tgt_deck = []
    random.seed(randomSeed)
    for i in range(num_targets):
        randomPoint_x, randomPoint_y = (random.randint(0, 1000), random.randint(0, 1000))
        width, height = (random.randint(1, 5) * 2, random.randint(1, 5) * 2)
        x_min, x_max = (randomPoint_x - width, randomPoint_x + width)
        y_min, y_max = (randomPoint_y - height, randomPoint_y + height)
        rect = tuple([(x_min, y_min, x_max, y_max), "Location:" + str(i)])
        if not (x_min < 0) or (y_min < 0):
            tgt_deck.append(rect)
        else:
            pass
        t_new['coord'] = tgt_deck

    return t_new


# Run script here
if __name__ == '__main__':
    p = index.Property()
    idx = index.Index(properties=p)
    actors_gen = generate_actors(num_actors)
    actorScenario = pd.DataFrame(actors_gen['coord'], columns=['Coordinates', 'ActorsLocation'])
    tgt_location = build_tgt_deck()
    locs = pd.DataFrame(tgt_location['coord'], columns=['Coordinates', 'Site'])
    _build_rtree(actors_gen)
    # _build_rtree(tgt_location) # Testing to evaluate targets separately from R-tree

    # Starting time after scenario is built
    start = time.clock()

    actors_caught = actors_in_collect(actors_gen, locs)
    actorsInTargets = len(actors_caught)  # if multiple actors were caught in the same targeted box this will create another column
    print("time to process %s actors and %s locations: %.03f s" % (num_actors, actorsInTargets, (time.clock() - start)))
    actors_caught = pd.DataFrame(actors_caught)
    colNames = []
    for i in range(len(actors_caught.columns)):
        colNames.append('Collections%s' % (i + 1))
    actors_caught.columns = colNames
    actors_caught = actors_caught.dropna(subset=['Collections1'])
    actors_caught = actors_caught.stack().reset_index(drop=True)
    actors_caught = pd.DataFrame(actors_caught.tolist(), columns=['Location', 'Actors', 'Coordinates'])

    new_col_list = ['Left', 'bottom', 'right', 'top']
    for n, col in enumerate(new_col_list):
        actors_caught[col] = actors_caught['Coordinates'].apply(lambda location: location[n])
    actors_caught = actors_caught.drop('Coordinates', axis=1)

    actors_caught.to_csv(os.path.join(outputFile, "Desktop\\Collections.csv"), index=False)
    locs.to_csv(os.path.join(outputFile, "Desktop\\Target_deck.csv"), index=False)
    actorScenario.to_csv(os.path.join(outputFile, "Desktop\\Actors_location.csv"), index=False)

    # Python time.clock is deprecated, but process_time and perf_counter does not send back ns
    print("time to process whole event: %.03f s" % ((time.clock() - start)))
