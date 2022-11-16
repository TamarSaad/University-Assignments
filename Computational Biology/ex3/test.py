import subprocess
import pkg_resources
import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import math
import ex3


def main():
    # running the script
    mean_distances = []
    best_hexa_rows = []
    best_hexa_economic_avg = []
    min_distance = math.inf
    for i in range(10):  # first 3 for evaluating, last 2 for creating the results
        sets_per_location, normalized_df, vectors_of_hex, hexa_rows, hexa_economic_avg = ex3.main()
        distances = 0
        # for each hexagon- calculate the distances from its cities and make average
        for hexagon in sets_per_location:
            hexagon_vec = vectors_of_hex[hexagon[0][0]][hexagon[0][1]]
            # go through each city
            for city in hexagon[1]:
                city_vec = normalized_df.loc[:, city]
                # get rms distance
                MSE = mean_squared_error(city_vec, hexagon_vec)
                RMS = math.sqrt(MSE)
                distances += RMS
        avg_distance = distances / len(normalized_df.columns)
        mean_distances.append(avg_distance)
        # save the best results
        if avg_distance < min_distance:
            min_distance = avg_distance
            best_hexa_rows = hexa_rows
            best_hexa_economic_avg = hexa_economic_avg
        print(f"iteration {i} ended\n\n\n\n\n\n\n")
    # get the results of the best result
    ex3.show_result(best_hexa_rows, best_hexa_economic_avg)
    print("The means of all the iterations are: ")
    print(mean_distances)


if __name__ == "__main__":
    main()

