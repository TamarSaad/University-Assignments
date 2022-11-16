import matplotlib.pyplot as plt
import numpy
import numpy as np
import os
import sys


def main():
    # load and costume the data
    image_fname, centroids_fname, out_fname = sys.argv[1], sys.argv[2], sys.argv[3]
    z = np.loadtxt(centroids_fname)
    orig_pixels = plt.imread(image_fname)
    pixels = orig_pixels.astype(float) / 255
    pixels = pixels.reshape(-1, 3)
    # number of centroids
    centnum = len(z)
    # create a new file for the new centroids
    f = open(out_fname, "w")
    # doing 20 iterations maximum
    for i in range(20):
        # create matrix with values for each centroid: pixel counter, R,G,B. initialize with 0
        centroids = np.zeros((centnum, 4))
        # going through each pixel
        for j in pixels:
            # initialize variables for minimum distance and its centroid index
            minDist = float("inf")
            indCent = None
            # going through each centroid and look for the minimum distance
            for k in range(centnum):
                dist = numpy.linalg.norm(j - z[k])
                if dist < minDist:
                    minDist = dist
                    indCent = k
            # for the closest centroid- update the counter+RGB:
            for m in range(centroids.shape[1]):
                # add one to the counter
                if m == 0:
                    centroids[indCent][m] += 1
                else:  # add the RGB values to the centroid
                    centroids[indCent][m] += j[m - 1]
        # after going through all the pixels: update the centroids
        for n in centroids:
            if n[0] != 0:
                n[1:] = n[1:] / n[0]
                n[0] = 0
        # print only 4 digits after dot
        centroids = centroids[:, 1:].round(4)
        # write to the file
        f.write(f"[iter {i}]:{','.join([str(c) for c in centroids])}\n")
        # check if there was change. If not- close and return
        if np.array_equal(z, centroids):
            f.close()
            break
        else:  # if there was a change- update the centroids
            z = centroids
    f.close()


if __name__ == '__main__':
    main()
