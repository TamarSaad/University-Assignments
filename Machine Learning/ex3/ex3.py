# Tamar Saad
# 207256991
# ex 3 machine learning

import sys
import numpy as np
from scipy.special import softmax, expit
import pytorch

EPOCHS = 25
N = 170
ETA = 0.01


# shuffle the data to get random distribution
def shuffle(trains, tags):
    assert len(trains) == len(tags)
    p = np.random.permutation(len(tags))
    return trains[p], tags[p]


def fprop(x, y, params):
    # Follows procedure given in notes
    W1, b1, W2, b2 = [params[key] for key in ('W1', 'b1', 'W2', 'b2')]
    z1 = np.dot(W1, x) + b1
    h1 = expit(z1)
    z2 = np.dot(W2, h1) + b2
    h2 = softmax(z2)
    loss = -np.log(h2[y])
    ret = {'x': x, 'y': y, 'z1': z1, 'h1': h1, 'z2': z2, 'h2': h2, 'loss': loss}
    for key in params:
        ret[key] = params[key]
    return ret


def bprop(fprop_cache):
    # Follows procedure given in notes
    x, y, z1, h1, z2, h2, loss = [fprop_cache[key] for key in ('x', 'y', 'z1', 'h1', 'z2', 'h2', 'loss')]
    dz2 = h2
    dz2[y] -= 1  # dL/dz2
    dW2 = np.dot(dz2, h1.T)  # dL/dz2 * dz2/dw2
    db2 = dz2  # dL/dz2 * dz2/db2
    dz1 = np.dot(fprop_cache['W2'].T,
                 (h2 - y)) * expit(z1) * (1 - expit(z1))  # dL/dz2 * dz2/dh1 * dh1/dz1
    dW1 = np.dot(dz1, x.T)  # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/dw1
    db1 = dz1  # dL/dz2 * dz2/dh1 * dh1/dz1 * dz1/db1
    return {'b1': db1, 'W1': dW1, 'b2': db2, 'W2': dW2}


def prediction(x, params):
    # Follows procedure given in notes
    W1, b1, W2, b2 = [params[key] for key in ('W1', 'b1', 'W2', 'b2')]
    z1 = np.dot(W1, x) + b1
    h1 = expit(z1)
    z2 = np.dot(W2, h1) + b2
    h2 = softmax(z2)
    return np.argmax(h2)


def main():
    train_file, tags_file, test_file = sys.argv[1], sys.argv[2], sys.argv[3]
    train = np.loadtxt(train_file) / 255
    tags = np.loadtxt(tags_file)
    tests = np.loadtxt(test_file) / 255
    # initialize the weight vectors
    W1 = np.random.uniform(-0.001, 0.001, (N, 784))
    b1 = np.zeros((N, 1))
    W2 = np.random.uniform(-0.001, 0.001, (10, N))
    b2 = np.zeros((10, 1))
    params = {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}

    # with open('loss.txt', 'w') as f:
    for epoch in range(EPOCHS):
        train, tags = shuffle(train, tags)
        loss = 0
        for t, tag in list(zip(train, tags)):
            t = np.reshape(t, (len(t), 1))
            fprop_cache = fprop(t, int(tag), params)
            bprop_cache = bprop(fprop_cache)

            # update
            dw1, db1, dw2, db2 = [bprop_cache[key] for key in ('W1', 'b1', 'W2', 'b2')]
            f_loss = fprop_cache['loss']
            params['W1'] -= ETA * dw1
            params['b1'] -= ETA * db1
            params['W2'] -= ETA * dw2
            params['b2'] -= ETA * db2
            loss += f_loss
        # f.write(f"the loss of epoch number {epoch} is: {loss / len(tags)}\n")

    # predicting the test's class
    y = []
    for test in tests:
        test = np.reshape(test, (len(test), 1))
        y_hat = prediction(test, params)
        y.append(y_hat)

    with open('test_y', 'w') as file:
        for item in y:
            file.write("%s\n" % item)


if __name__ == '__main__':
    main()
