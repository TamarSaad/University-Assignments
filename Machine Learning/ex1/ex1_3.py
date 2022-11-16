import matplotlib.pyplot as plt
import numpy
import numpy as np
import os
import sys


def getCentroids():
    image_fname, centroids_fname, out_fname = sys.argv[1], sys.argv[2], sys.argv[3]
    z = np.loadtxt(centroids_fname)
    orig_pixels = plt.imread(image_fname)
    pixels = orig_pixels.astype(float) / 255
    pixels = pixels.reshape(-1, 3)
    # number of centroids
    centnum = len(z)
    costs = np.zeros((0, 2))
    # create a new file
    # doing 20 iterations maximum
    for i in range(20):
        # create matrix with values for each centroid: pixel counter, R,G,B. initialize with 0
        centroids = np.zeros((centnum, 4))
        # going through each pixel
        for j in pixels:
            # initialize variables for minimum distance, its centroid value and index
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
                if m != 0:  # add the RGB values to the centroid
                    centroids[indCent][m] += j[m - 1]
                # add one to the counter
                else:
                    centroids[indCent][m] += 1
        # after going through all the pixels: update the centroids
        for n in centroids:
            if n[0] != 0:
                n[1:] = n[1:] / n[0]
                n[0] = 0
        # print only 4 digits after dot
        centroids = centroids[:, 1:].round(4)
        # calculate cost
        # initialize the summary to 0
        costSum = 0
        # going through each pixels
        for p in pixels:
            minD = float("inf")
            # going through each centroid and look for the minimum distance
            for c in centroids:
                dist = numpy.linalg.norm(p - c)
                if dist < minD:
                    minD = dist
                    p=c
            # add the minimal distance to the summary
            costSum += minD
        # calculate the cost
        costs = np.vstack((costs, np.array([i, costSum / pixels.shape[0]])))

        # write to the file
        # check if there was change. If not- close and return
        if np.array_equal(z, centroids):
            break
        else:  # if there was a change- update the centroids
            z = centroids
    return costs


# calculate for different numbers of centroids
def setK():
    costs2 = calculate_cost(2)
    np.savetxt("costs2.txt", costs2, delimiter=' ', fmt='%1.4g')
    costs4 = calculate_cost(4)
    np.savetxt("costs4.txt", costs4, delimiter=' ', fmt='%1.4g')
    costs8 = calculate_cost(8)
    np.savetxt("costs8.txt", costs8, delimiter=' ', fmt='%1.4g')
    costs16 = calculate_cost(16)
    np.savetxt("costs16.txt", costs16, delimiter=' ', fmt='%1.4g')


# calculte cost for each centroid number
def calculate_cost(k):
    # initialize the centroids and wright them as text file
    centroids = np.random.rand(k, 3)
    np.savetxt("centroids.txt", centroids, delimiter=' ', fmt='%1.4f')
    # calculate the new centroids with the function, and get the picture's pixels as well
    costs = getCentroids()
    plt.plot(costs[:, 0], costs[:, 1])
    plt.suptitle(f"cost vs. iteration for k={k}")
    plt.xlabel("iteration")
    plt.ylabel("cost")
    plt.show()
    return costs


def main():
    setK()


if __name__ == '__main__':
    main()
