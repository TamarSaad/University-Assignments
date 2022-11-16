import sys
import numpy as np


def main():
    predicted_file, real_file = sys.argv[1], sys.argv[2]
    predicted = np.loadtxt(predicted_file, dtype='str')
    real = np.loadtxt(real_file, dtype='str')
    correct = 0
    size = len(predicted)
    for line_p, line_r in list(zip(predicted, real)):
        if line_p == line_r:
            correct += 1
    print("precentage of accuracy: " + str(correct / size * 100))



if __name__== '__main__':
    main()