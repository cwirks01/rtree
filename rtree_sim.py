import rtree as rt
import os
import pandas as pd
import numpy as np
from rtree import index
from rtree.index import Rtree
import random
import time

start = time.clock()

random.seed(0)  # Need random seed to perform test
num_targets = 5
num_actors = 10

ROOT = os.getcwd()


def _build_rtree(locations):
    """ build environment of scenario using the bounded area in generate_actors """
    # Will initiate with the largest bounded area

    return


def generate_actors(num_of_actors):
    """
    Actors are randomly generated throughout a grid of a 1000
    Inserting a point into a rtree left == right and bottom == top
    :param num_of_actors:
    :return:
    """
    actors = dict()
    actors_loc = []
    for i in range(num_of_actors):
        randomPoint_x, randomPoint_y = (random.randint(0, 1000), random.randint(0, 1000))
        loc = tuple([randomPoint_x, randomPoint_y, randomPoint_x, randomPoint_y])
        if not (randomPoint_x < 0) or (randomPoint_y < 0):
            actors_loc.append(loc)
        else:
            pass
        actors['coord'] = actors_loc
    return actors


def actors_in_collect(actors):
    return


def build_tgt_deck():
    """
    build_tgt_deck randomly generate rectangles with varying sides on a grid of a 1000
    X and Y values less than zero will not be appended to the list of targets
    :return:
    """
    t_new = dict()
    tgt_deck = []
    for i in range(num_targets):
        randomPoint_x, randomPoint_y = (random.randint(0, 1000), random.randint(0, 1000))
        width, height = (random.randint(1, 5) * 2, random.randint(1, 5) * 2)
        x_min, x_max = (randomPoint_x - width, randomPoint_x + width)
        y_min, y_max = (randomPoint_y - height, randomPoint_y + height)
        rect = tuple([(x_min, y_min, x_max, y_max)])
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
    print(generate_actors(num_actors))
    print(build_tgt_deck())

    # Python time.clock is deprecated, but process_time and perf_counter does not send back ns
    time_stop = time.clock()

    print("time to process: %.03f ns" % ((time_stop - start) * 10**6))
