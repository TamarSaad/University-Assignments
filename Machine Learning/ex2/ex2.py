# Tamar Saad
# 207256991
# ex 2 machine learning

import sys
import numpy as np


# k nearest neighbors
def KNN(train_set, train_tags, test, k):
    # initialize the distance matrix with zeros
    distances = np.zeros((len(train_tags), 2))
    # save in the matrix the distance and the tags
    for i in range(len(train_set)):
        distances[i][0] = np.linalg.norm(train_set[i] - test)
        distances[i][1] = train_tags[i]
    # sort to find smallest k distances
    distances = distances[np.argsort(distances[:, 0]), :]
    # initialize the counter for each group
    counts = np.zeros(3)
    # sum the tags of the k nearest neighbors
    for index in range(k):
        tag = int(distances[index][1])
        counts[tag] += 1
    # return the tag with the most counts
    return np.argmax(counts)


# this class is the parent of the algorithms Perceptron, SVM and PA
class Algorithms:
    # consructor
    def __init__(self, trains, tags):
        # adding ones to the trains mat so we can work with bias
        arr = np.ones((len(tags), 1))
        self.trains = np.column_stack((trains, arr))
        self.tags = tags
        # initialize the weights to zeros
        self.weights = np.zeros((3, 6))
        # doing epochs
        for T in range(500):
            # shuffle the samples
            self.shuffle(self.trains, self.tags)
            # go through each sample in the train set
            for ind, sample in enumerate(self.trains):
                # find max dotup and the tag
                yhat = np.argmax(np.dot(self.weights, sample))
                # find the actual tag
                y = self.tags[ind]
                # update the weights vectors
                self.update_vectors(y, yhat, sample)

    # finding the tag of a test sample
    def find_tag(self, test):
        # adding 1 to the vector so we can multiply them
        test = np.append(test, 1)
        return np.argmax(np.dot(self.weights, test))

    # shuffle the data to get random distribution
    def shuffle(self, trains, tags):
        p = np.random.permutation(len(tags))
        self.trains = trains[p]
        self.tags = tags[p]

    def update_vectors(self, y, yhat, sample):
        pass


class Perceptron(Algorithms):
    # initialize the data and find the weights vectors
    def __init__(self, trains, tags, eta):
        self.eta = eta
        super().__init__(trains, tags)

    def update_vectors(self, y, yhat, sample):
        if yhat != y:
            self.weights[yhat] -= self.eta * sample
            self.weights[y] += self.eta * sample


class SVM(Algorithms):
    def __init__(self, trains, tags, eta, lamda):
        self.eta = eta
        self.lamda = lamda
        super().__init__(trains, tags)

    def update_vectors(self, y, yhat, sample):
        dot_products = np.dot(self.weights, sample)
        if y == yhat:
            yhat = np.argpartition(dot_products, -2)[-2]
        self.weights = self.weights * (1 - self.eta * self.lamda)
        if dot_products[y] - dot_products[yhat] < 1:
            self.weights[y] += self.eta * sample
            self.weights[yhat] -= self.eta * sample


class PA(Algorithms):
    def __init__(self, trains, tags):
        super().__init__(trains, tags)

    def update_vectors(self, y, yhat, sample):
        dot_products = np.dot(self.weights, sample)
        loss = max(0, 1 - (dot_products[y] - dot_products[yhat]))
        tau = loss / (2 * np.power(np.linalg.norm(sample), 2))
        self.weights[y] += tau * sample
        self.weights[yhat] -= tau * sample


def main():
    # get input
    train_file, tags_file, test_file, out_file = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    trains = np.loadtxt(train_file, delimiter=',')
    tags = np.loadtxt(tags_file, dtype="int")
    tests = np.loadtxt(test_file, delimiter=',')

    # normalize the data by z-score
    zscore_trains = np.zeros(trains.shape)
    zscore_tests = np.zeros(tests.shape)
    mean = np.mean(trains, 0)
    std = np.std(trains, 0)
    for i in range(len(trains)):
        zscore_trains[i, :] = ((trains[i, :] - mean) / std)
    for i in range(len(tests)):
        zscore_tests[i, :] = ((tests[i, :] - mean) / std)
    # minmax_trains=(trains-min(trains))/(max(trains)-min(trains))

    # initialize algorithms
    perceptron = Perceptron(zscore_trains.copy(), tags.copy(), eta=0.1)
    svm = SVM(zscore_trains.copy(), tags.copy(), eta=0.02, lamda=0.02)
    pa = PA(zscore_trains.copy(), tags.copy())

    # predicting classes for test samples
    with open(out_file, 'w') as file:
        for ind, test in enumerate(zscore_tests):
            knn_yhat = KNN(zscore_trains, tags, test, k=5)
            perceptron_yhat = perceptron.find_tag(test)
            svm_yhat = svm.find_tag(test)
            pa_yhat = pa.find_tag(test)
            file.write(f"knn: {knn_yhat}, perceptron: {perceptron_yhat}, svm: {svm_yhat}, pa: {pa_yhat}\n")



if __name__ == '__main__':
    main()
