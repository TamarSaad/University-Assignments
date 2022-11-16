import subprocess
import pkg_resources
import sys
import os

# check if the packages being used are installed and if not- install
packages = {'matplotlib', 'numpy', 'pygame', 'easygui', 'hexalattice', 'pandas', 'sklearn'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = packages - installed
if missing:
    print('Download dependencies here: ', os.getcwd())
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import copy
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import numpy as np
from itertools import product
from random import sample
import pygame
from easygui import multenterbox
import hexalattice
from hexalattice.hexalattice import *
import math
from math import pi
import pandas as pd
from sklearn import preprocessing
import collections
from sklearn.metrics import mean_squared_error


# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BAJE = (245, 245, 220)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

num_of_iterations = 100


def draw_my_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    # This draws a hexagon using the polygon command
    pygame.draw.polygon(surface, color, [
        (x + r * math.sin(2 * math.pi * i / n),
         y + r * math.cos(2 * math.pi * i / n))
        for i in range(n)
    ], width)


def show_result(rows, hexa_economic_avg):
    # Initialize the game engine
    pygame.init()

    # Set the height and width of the screen
    size = [600, 600]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Example code for the draw module")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close or esc
                done = True  # Flag that we are done so we exit this loop

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        minima = min(hexa_economic_avg)
        maxima = max(hexa_economic_avg)
        norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima)
        cmap = cm.jet
        for row in rows:
            for loc in row:
                if loc[2] == 0:
                    color = BAJE
                else:
                    rgb = cmap(norm(abs(loc[2])))[:3]
                    color = matplotlib.colors.rgb2hex(rgb)
                draw_my_polygon(screen, color, 6, 25, [loc[0], loc[1]])

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()


# normalize each column of the data-frame from min-max
def normalize_column(values):
    min_val = np.min(values)
    max_val = np.max(values)
    norm_val = (values - min_val) / (max_val - min_val)
    return pd.DataFrame(norm_val)


# find distance between two vectors
def find_distance(x, y):
    distance = 0
    for i in range(len(x)):
        distance += ((x[i] - y[i]) ** 2)
    norm = np.sqrt(distance)
    return norm


def update_vector_and_neighbors(instance, vectors, vector_index, hexa_indexes):
    # chosen vector update
    i, j = vector_index[0], vector_index[1]
    vectors[i][j] = vectors[i][j] + 0.3 * (instance - vectors[i][j])
    # neighbors update
    # find who is a relevant neighbor
    potential_neighbors = []
    scnd_potential_neighbors = []
    if i < 4:
        potential_neighbors = [(i, j - 1), (i, j + 1), (i - 1, j - 1), (i - 1, j), (i + 1, j), (i + 1, j + 1)]
        if i == 3:
            scnd_potential_neighbors = [(i, j - 2), (i, j + 2), (i - 1, j - 2), (i - 1, j + 1), (i - 2, j - 2),
                                        (i - 2, j - 1), (i - 2, j), (i + 1, j - 1), (i + 1, j + 2), (i + 2, j - 1),
                                        (i + 2, j), (i + 2, j + 1)]
        else:
            scnd_potential_neighbors = [(i, j - 2), (i, j + 2), (i - 1, j - 2), (i - 1, j + 1), (i - 2, j - 2),
                                        (i - 2, j - 1), (i - 2, j), (i + 1, j - 1), (i + 1, j + 2), (i + 2, j),
                                        (i + 2, j + 1), (i + 2, j + 2)]
    elif i > 4:
        potential_neighbors = [(i, j - 1), (i, j + 1), (i - 1, j), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j)]
        if i == 5:
            scnd_potential_neighbors = [(i, j - 2), (i, j + 2), (i - 1, j - 2), (i - 1, j + 1), (i - 2, j - 1),
                                        (i - 2, j), (i - 2, j + 1), (i + 1, j - 1), (i + 1, j + 2), (i + 2, j - 1),
                                        (i + 2, j), (i + 2, j + 1)]
        else:
            scnd_potential_neighbors = [(i, j - 2), (i, j + 2), (i - 1, j - 1), (i - 1, j + 2), (i - 2, j),
                                        (i - 2, j + 1), (i - 2, j + 2), (i + 1, j - 2), (i + 1, j + 1), (i + 2, j - 2),
                                        (i + 2, j - 1), (i + 2, j)]
    else:
        potential_neighbors = [(i, j - 1), (i, j + 1), (i - 1, j - 2), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j)]
        scnd_potential_neighbors = [(i, j - 2), (i, j + 2), (i - 1, j - 2), (i - 1, j + 1), (i - 2, j - 2),
                                    (i - 2, j - 1), (i - 2, j), (i + 1, j - 2), (i + 1, j + 1), (i + 2, j - 2),
                                    (i + 2, j - 1), (i + 2, j)]
    # update first degree neighbors
    for neighbor in potential_neighbors:
        if neighbor in hexa_indexes:  # check if neighbor position exists
            loc_i, loc_j = neighbor[0], neighbor[1]
            vectors[loc_i][loc_j] = vectors[loc_i][loc_j] + 0.2 * (instance - vectors[loc_i][loc_j])  # update neighbors
    # update second degree neighbors
    # for neighbor in scnd_potential_neighbors:
    #     if neighbor in hexa_indexes:  # check if neighbor position exists
    #         loc_i, loc_j = neighbor[0], neighbor[1]
    #         vectors[loc_i][loc_j] = vectors[loc_i][loc_j] + 0.1 * (instance - vectors[loc_i][loc_j])  # update neighbors
    return vectors


# find the clusters and update the centroids
def find_clusters(vectors, data, hexa_indexes):
    clusters = []
    num_of_instance_per_hexa = [0] * 61
    for name, instance in data.iteritems():
        min_distance = find_distance(instance, vectors[0][0])
        chosen_vector = (0, 0)
        for index_r, row in enumerate(vectors):
            for index, vec in enumerate(row):
                new_min_distance = find_distance(instance, vec)
                if new_min_distance < min_distance:
                    min_distance = new_min_distance
                    chosen_vector = (index_r, index)
        clusters.append((name, chosen_vector))
        num_of_instance_per_hexa[hexa_indexes.index(chosen_vector)] += 1
        vectors = update_vector_and_neighbors(instance, vectors, chosen_vector, hexa_indexes)
    return clusters, vectors, num_of_instance_per_hexa


def create_vectors():
    # Create 61 random vectors- each 14 features long, every value between 0-1
    vectors = []
    hexa_indexes = []
    for i in range(9):
        vector_row = []
        num_of_hexagons = 9 - abs(4 - i)
        for j in range(num_of_hexagons):
            vector_row.append(np.random.default_rng().uniform(0, 1, 14))
            hexa_indexes.append((i, j))
        vectors.append(vector_row)
    return vectors, hexa_indexes


def calc_cluster_average(clusters, num_of_instance_per_hexa, hexa_indexes, economic_status):
    hexa_economic_avg = []
    cluster_by_hexa = []
    for index, hexa in enumerate(hexa_indexes):
        economic_sum = 0
        # Find an element in list of tuples.
        cities = [item[0] for item in clusters
                  if item[1] == hexa]
        if len(cities):
            for city in cities:
                economic_sum += economic_status[city]
            economic_avg = economic_sum / num_of_instance_per_hexa[index]
            hexa_economic_avg.append(economic_avg)
            cluster_by_hexa.append((hexa, cities))
        else:
            hexa_economic_avg.append(0)
    return hexa_economic_avg, cluster_by_hexa


def create_hexa_board(hexa_economic_avg):
    rows = []
    row = []
    j = 0
    for i in range(200, 450, 50):
        row.append([i, 100, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(175, 475, 50):
        row.append([i, 140, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(150, 500, 50):
        row.append([i, 180, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(125, 525, 50):
        row.append([i, 220, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(100, 550, 50):
        row.append([i, 260, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(125, 525, 50):
        row.append([i, 300, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(150, 500, 50):
        row.append([i, 340, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(175, 475, 50):
        row.append([i, 380, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    row = []
    for i in range(200, 450, 50):
        row.append([i, 420, hexa_economic_avg[j]])
        j += 1
    rows.append(row)
    return rows


# calculate the average distance between the cities and their neurons using rms
def getDistanceScore(sets_per_location, vectors_of_hex, normalized_df):
    distances = 0
    for hexagon in sets_per_location:
        hexagon_vec = vectors_of_hex[hexagon[0][0]][hexagon[0][1]]
        # go through each city
        for city in hexagon[1]:
            city_vec = normalized_df.loc[:, city]
            # get rms distance
            MSE = mean_squared_error(city_vec, hexagon_vec)
            RMS = math.sqrt(MSE)
            distances += RMS
    return distances / len(normalized_df.columns)


def main():
    # Read the csv file
    file = input("Please Enter A File Name For The Program: \n")
    print(file)
    # read input file to create the initial board
    df = pd.read_csv(file)

    # df = pd.read_csv('Elec_24.csv')
    df = df.T  # transpose columns and rows
    df.columns = df.iloc[0]
    df = df[1:]
    # Save Economic background
    economic = df.iloc[0]
    df = df[1:]
    # Normalize using Min/Max Normalization.
    # normalized_df = (df_shuff - df_shuff.min()) / (df_shuff.max() - df_shuff.min())
    normalized_df = df / df.max()
    normalized_df = normalized_df.sample(frac=1, axis=1)  # shuffle the settlements

    vectors, hexa_indexes = create_vectors()
    # old_vectors = copy.deepcopy(vectors)
    # k = 61  # num of hexagons vectors
    first_iteration = True
    old_clusters = []
    for iter in range(num_of_iterations):
        # print(iter)
        # flag = 0
        clusters, vectors, num_of_instance_per_hexa = find_clusters(vectors, normalized_df, hexa_indexes)
        # for index_r, row in enumerate(vectors):
        #     for index, vec in enumerate(row):
        #         if np.array_equal(old_vectors[index_r][index], vectors[index_r][index]):
        #             flag += 1
        # Check convergence
        if first_iteration:  # define the old clusters vector
            old_clusters = copy.deepcopy(clusters)
            first_iteration = False
            continue
        # if the lists are equal
        if collections.Counter(old_clusters) == collections.Counter(clusters):
            print("Found convergence")
            break
        else:
            # old_vectors = copy.deepcopy(vectors)
            old_clusters = copy.deepcopy(clusters)

    print(f"We ran {iter} epochs! Good job!")
    hexa_economic_avg, cluster_by_hexa = calc_cluster_average(clusters, num_of_instance_per_hexa, hexa_indexes,
                                                              economic)

    hexa_rows = create_hexa_board(hexa_economic_avg)

    print("CLUSTERS BY CITIES:")
    for item in cluster_by_hexa:
        print("hexagone coordinates: " + str(item[0]))
        print("cluster cities and their economy status: ")
        for city in item[1]:
            print(city + "- " + str(economic[city]))
    avg_distance = getDistanceScore(cluster_by_hexa, vectors, normalized_df)
    print(f"\nThe average distance is: {avg_distance}")
    show_result(hexa_rows, hexa_economic_avg)
    # return cluster_by_hexa, normalized_df, vectors, hexa_rows, hexa_economic_avg


if __name__ == "__main__":
    main()
