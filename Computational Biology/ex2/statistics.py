import subprocess
import pkg_resources
import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ex2_best


def main():
    column_names = ["regular", "lamarck", "darwin"]
    best = pd.DataFrame(columns=column_names)
    avg = pd.DataFrame(columns=column_names)
    generations = pd.DataFrame(columns=column_names)
    # running the script
    files = ["example_5.txt", "example_5_tricky.txt", "example_6_easy.txt", "example_7_easy.txt",
             "6_tricky.txt", "7_tricky.txt"]
    for i in range(20):
        file = random.choice(files)
        b, a, g = ex2_best.main(file)
        best.loc[i] = b
        avg.loc[i] = a
        generations.loc[i] = g
        print(f"\n {i} \n \n")
    best.to_csv('best.csv', index=False)
    avg.to_csv('avg.csv', index=False)
    generations.to_csv('generations.csv', index=False)


if __name__ == "__main__":
    main()
