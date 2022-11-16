import subprocess
import pkg_resources
import sys
import os

# check if the packages being used are installed and if not- install
packages = {'matplotlib', 'numpy', 'upsidedown'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = packages - installed
if missing:
    print('Download dependencies here: ', os.getcwd())
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import copy
import random
import matplotlib.pyplot as plt
import numpy as np
import upsidedown

population_size = 100

# function to create the first board with the file parameters
def initialize(input_list):
    # create the base board with the parameters entered
    base_board = np.zeros([int(input_list[0]), int(input_list[0])], dtype=int)
    location = 2  # first number parameter location in the list
    # enter the initial numbers
    for num in range(int(input_list[1])):
        loc = input_list[location].split(' ')  # split the parameters to single numbers
        base_board[int(loc[0]) - 1][int(loc[1]) - 1] = int(loc[2])
        location += 1
    input_list = input_list[location:]  # leave only the ">" signs from the original parameters
    return base_board, input_list

# function to create the first 100 boards generation
def create_first_generation(base_board, num_of_boards):
    board_list = []
    for solution in range(num_of_boards):  # creating 100 boards solutions
        board = copy.deepcopy(base_board)  # copy the initial board
        for i in range(base_board.shape[0]):
            row = np.arange(1, base_board.shape[0] + 1)  # create array of nums from 1-N
            # check if there are numbers in the row on the base board
            for num in row:
                if num in board[i]:
                    row = row[row != num]  # initial row only with nums that arent already in the base board
            row = np.random.permutation(row)  # permute the numbers left in the array
            # enter permutation into the board
            permut_num = 0
            for j in range(base_board.shape[1]):
                if board[i][j] == 0:  # if there are no number in the base board
                    board[i][j] = row[permut_num]
                    permut_num += 1
                else:  # in that location there is a number in the base board
                    continue
        board_list.append(board)
    return board_list


# function to calculate fitness function for each board
def evaluate(board_list, input_list):
    boards_and_scores = []
    for board in board_list:
        fitness = 0
        # check columns discrepancies
        for j in range(board.shape[1]):  # go through each column
            col = board[:, j].tolist()
            for num in range(1, board.shape[0]+1):
                count = col.count(num)  # count the number of appearances of a number in that column
                if count > 1:  # means the number appears mor then once
                    fitness += count - 1  # num of appearances minus one that is legal appearance
                else:
                    continue
        # check “greater than” signs discrepancies
        locations = 1  # first grater sign location in the list
        for num in range(int(input_list[0])):  # number of signs in the user input file
            loc = input_list[locations].split(' ')  # split the parameters to single numbers
            locations += 1
            # if the numbers in the board maintain the Constraint
            if board[int(loc[0]) - 1][int(loc[1]) - 1] > board[int(loc[2]) - 1][int(loc[3]) - 1]:
                continue
            else:
                fitness += 1
        boards_and_scores.append((board, fitness))
    return boards_and_scores


# function to create lamarck optimization
def lamarck_evaluate(board_list, input_list, base_board):
    for board in board_list:
        # array to save Inconsistencies in the board
        wrong_loc = []
        missing_num = []
        wrong_grater_sign = []
        # check columns discrepancies
        for j in range(board.shape[1]):
            col = board[:, j].tolist()
            for num in range(1, board.shape[0]+1):
                count = col.count(num)  # count the number of appearances of a number in that column
                if count > 1:  # the number appears mor then once
                    new_col = (col - base_board[:, j]).tolist()  # remove the index of initial num from the base board
                    new_count = new_col.count(num)  # count again to see if the count has changed
                    if new_count == count:  # the number is not fixed
                        for c in range(new_count-1):  # run the loop count-1 times (one appearance is good)
                            # find the indexes of mismatch and save them
                            loc = new_col.index(num)
                            wrong_loc.append((loc, j))
                            new_col[loc] = 0  # remove the index of previous num to keep finding new locations
                    else:
                        # run the loop new_count times (one appearance was deleted since it was fixed num)
                        for c in range(new_count):
                            # find the indexes of mismatch and save them
                            loc = new_col.index(num)
                            wrong_loc.append((loc, j))
                            new_col[loc] = 0  # remove the index of previous num
                elif count == 0:  # the number doesnt appear at all in the column
                    missing_num.append(num)
                else:
                    continue
        # check “greater than” signs discrepancies
        locations = 1  # first greater sign location in the list
        for num in range(int(input_list[0])):
            loc = input_list[locations].split(' ')
            locations += 1
            if board[int(loc[0]) - 1][int(loc[1]) - 1] > board[int(loc[2]) - 1][int(loc[3]) - 1]:
                continue
            else:
                # find the index of mismatch and save it
                # if the index is not in a fixed base board num
                if base_board[int(loc[0]) - 1, int(loc[1]) - 1] == 0:
                    wrong_grater_sign.append((int(loc[0]) - 1, int(loc[1]) - 1))
                else:
                    wrong_grater_sign.append((int(loc[2]) - 1, int(loc[3]) - 1))

        # create up to x optimization for the board
        opt_num = 0
        i = 0
        while (opt_num < board.shape[1]) & (i < len(wrong_loc)):
            row = wrong_loc[i][0]
            col = wrong_loc[i][1]
            if base_board[row, col] == 0:  # first check if the mismatch is not a fixed num
                replace = board[row, :].tolist().index(missing_num[i])  # find the index of number that we wish to replace
                if base_board[row, replace] == 0:  # second check if the new replacement is not a fixed num
                    # switch numbers in the column
                    temp = board[row, col]
                    new = board[row, replace]
                    board[row, col] = new
                    board[row, replace] = temp
            opt_num += 1
            i += 1
        if opt_num < board.shape[1]:
            j = 0
            while (opt_num < board.shape[1]) & (j < len(wrong_grater_sign)):
                row = wrong_grater_sign[j][0]
                col = wrong_grater_sign[j][1]
                if base_board[row, col] == 0:  # first check if the mismatch is not a fixed num
                    replace = random.choice(range(board.shape[1]))  # randomly select number from the row
                    if base_board[row, replace] == 0:  # second check if the new replacement is not a fixed num
                        temp = board[row, col]
                        new = board[row, replace]
                        board[row, col] = new
                        board[row, replace] = temp
                opt_num += 1
                j += 1

    # create boards and fitness score list
    boards_and_scores = evaluate(board_list, input_list)
    return boards_and_scores

# function to create darwin optimization
def darwinian_evaluate(board_list, input_list, base_board):
    # copy old boards to save them
    old_boards = copy.deepcopy(board_list)
    # get new boards after optimization and new fitness score
    boards_and_scores = lamarck_evaluate(board_list, input_list, base_board)
    # combine old board with new fitness score
    ng_boards_and_scores = []
    for i in range(len(boards_and_scores)):
        ng_boards_and_scores.append((old_boards[i], boards_and_scores[i][-1]))

    # create evaluation of fitness for old boards also
    real_boards_and_scores = evaluate(board_list, input_list)
    return ng_boards_and_scores, real_boards_and_scores


# create the wanted number of boards after crossover
def get_crossovers(boards, num_of_boards):
    biased_boards = 8 * boards[:5]  # first 5 best boards
    biased_boards += 4 * boards[5: 20]  # second 15 best boards
    biased_boards += 1 * boards[20:]  # rest of the boards
    np.random.shuffle(biased_boards)  # shuffle array to get random locations
    new_boards = []
    # create crossovers
    i = 0
    while i < num_of_boards:
        # choose boards randomly to be the "parents", meaning the same board can get chosen twice
        random_sample = np.random.choice(len(biased_boards), 2, replace=False)
        random_boards = [biased_boards[i] for i in random_sample]
        crossed_board = copy.deepcopy(random_boards[0])  # first copy the first parent
        # we want to create a crossover point
        crossing_location = np.random.choice(random_boards[0].shape[1])
        # add second parent to cross location
        crossed_board[crossing_location:] = copy.deepcopy(random_boards[1][crossing_location:])
        new_boards.append(crossed_board)
        i += 1
    return new_boards


# function to create mutations in the boards
def create_mutations(board_list, base_board, probability):
    # calculate num of mutations in each board based on probability
    num_of_mutations = round(base_board.shape[1] ** 2 * probability)
    muts = []
    j = 0
    for board in board_list:
        # keep the best 4 boards unharmed
        if j < 4:
            muts.append(copy.deepcopy(board))
            j += 1
            continue
        # choose locations for mutations
        row_locs = random.choices(range(base_board.shape[1]), k=num_of_mutations)
        col_locs = random.choices(range(base_board.shape[1]), k=num_of_mutations)
        for i in range(num_of_mutations):
            if base_board[row_locs[i], col_locs[i]] == 0:  # if it's not a fixed value
                # the index of the number we will replace it with, check if it is a fixed value
                replace = random.choice(range(base_board.shape[1]))
                while base_board[row_locs[i], replace] != 0:  # if replace is in fixed value location keep choosing
                    replace = random.choice(range(base_board.shape[1]))
                # switch chosen numbers
                temp = board[row_locs[i], col_locs[i]]
                new = board[row_locs[i], replace]
                board[row_locs[i], col_locs[i]] = new
                board[row_locs[i], replace] = temp
        muts.append(copy.deepcopy(board))
        j += 1

    return muts


# create a new list of boards for the next generation
def next_generation(base_board, boards_and_scores, short_input_list):
    # take the best 25 boards to next generation as they are by their fitness score
    boards = [x[0] for x in boards_and_scores]
    # get 25 boards
    ng_boards = boards[:25]
    # initialize 15 new boards to avoid early convergence
    ng_boards += create_first_generation(base_board, 15)
    # create crossovers for the rest
    crossovers = get_crossovers(ng_boards, 60)
    ng_boards += crossovers
    # get the fitness values now so we can protect the top boards
    boards_and_scores_temp = evaluate(ng_boards, short_input_list)
    boards_and_scores_temp.sort(key=lambda x: x[1])
    sorted_boards = [x[0] for x in boards_and_scores_temp]
    # create mutations, but leave the X best boards protected
    ng_boards = create_mutations(sorted_boards, base_board, 0.1)
    return ng_boards


# helper function to print the boardes
def get_sign(big, small):
    if big[0] > small[0]:
        return upsidedown.transform("V")
    if big[0] < small[0]:
        return "V"
    if big[1] > small[1]:
        return "<"
    if big[1] < small[1]:
        return ">"


# function to print the board solution
def print_board(board, input_list, title, best_fitness, mean_fitness, generation):
    # the dimension of the printed matrix
    size = board.shape[0] * 2 - 1
    # separate the board by spaces
    board_split = np.zeros((size, size))
    for j in range(0, size, 2):
        split = []
        for i in range(board.shape[0]):
            split.append(board[int(j/2)][i])
            split.append(0)
        split = split[:-1]
        board_split[j, :] = split
    # add the greater than signs
    num_of_signs = int(input_list[0])
    board_int = board_split.astype(int)
    board_str = board_int.astype(str)
    for sign in range(1, num_of_signs+1):
        locs = input_list[sign].split(' ')
        big = [int(locs[0])-1, int(locs[1])-1]
        small = [int(locs[2])-1, int(locs[3])-1]
        locy = int((big[0]*2 + small[0]*2) / 2)
        locx = int((big[1]*2 + small[1]*2) / 2)
        greater_than = get_sign(big, small)
        board_str[locy, locx] = greater_than
    # remove zeroes
    board_str[board_str == "0"] = " "

    # create plot figure output
    fig, ax = plt.subplots(1, 1)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=board_str, loc="center", cellLoc="center")
    # add title
    plt.suptitle(title, fontsize=20, fontweight='bold')
    ax.set_title(f'Best Fitness Score = {best_fitness}\n Avg Fitness Score = {mean_fitness}\n Generation = {generation}'
                 , fontsize=12, color='red', x=.1, y=.8)
    plt.savefig(title + '.png')


# function to create a graph output
def plot_plots(title, best, avg):
    plot_num = plt.figure()
    plt.plot(best, 'r', label="best score")
    plt.plot(avg, 'b', label="average score")
    plt.legend()
    plt.xlabel('Generations (X100)')
    plt.ylabel('Fitness Score')
    plt.suptitle(title, fontsize=15, fontweight='bold')
    plot_num.savefig(title + ' graph.png')


def main():
    file = input("Please Enter A File Name For The Program: \n")
    print(file)
    # read input file to create the initial board
    with open(file) as input_file:
        input_list = [line.rstrip() for line in input_file]
    # create the base_board
    base_board, short_input_list = initialize(input_list)

    #### regular algorithm
    regular_best = []
    regular_avg = []
    # create first generation of solutions
    board_list = create_first_generation(base_board, population_size)
    # evaluate solutions
    boards_and_scores = evaluate(board_list, short_input_list)
    boards_and_scores.sort(key=lambda x: x[1])  # sort
    # as long as we dont have a solution
    i = 1
    reg5000 = []  # in case the first run is better then the second initialized run
    print("Running regular algorithm: ")
    # run a long as there is no solution and no 10,000 generations has passed
    while (boards_and_scores[0][-1] != 0) & (i < 10000):
        board_list = next_generation(base_board, boards_and_scores, short_input_list)
        # if we didn't find the result in 5000 rounds- start over
        if i == 5001:
            reg5000 = board_list  # save the boards of the first run
            board_list = create_first_generation(base_board, population_size)
        boards_and_scores = evaluate(board_list, short_input_list)
        boards_and_scores.sort(key=lambda x: x[1])
        if i % 100 == 0:
            mean = np.mean([x[1] for x in boards_and_scores])
            print(
                f"best scores of round {i} are: {boards_and_scores[0][-1]}, {boards_and_scores[1][-1]}, {boards_and_scores[2][-1]}")
            print(f"The avg of the scores is {mean}")
            regular_best.append(boards_and_scores[0][-1])
            regular_avg.append(mean)
        i += 1
    if boards_and_scores[0][-1] == 0:
        print(f"Successssssss!! you're the queen of the world!!! and it only took you like {i} rounds! Crazyyy")
    regular_best_board = copy.deepcopy(boards_and_scores[0][0])
    regular_best_fitness = boards_and_scores[0][-1]
    regular_generations = i
    # if we didn't find a solution- take best board from either last run or run 5000
    if regular_generations == 10000:
        boards_and_scores5000 = evaluate(reg5000, short_input_list)
        boards_and_scores5000.sort(key=lambda x: x[1])
        # if the best board is from run 5000
        if boards_and_scores5000[0][-1] < regular_best_fitness:
            regular_best_board = copy.deepcopy(boards_and_scores5000[0][0])
            regular_best_fitness = boards_and_scores5000[0][-1]
    mean = np.mean([x[1] for x in boards_and_scores])
    regular_best.append(boards_and_scores[0][-1])
    regular_avg.append(mean)

    ### lamarck optimization
    print("\nRunning Lamarck algorithm: ")
    # create first generation of solutions
    board_list = create_first_generation(base_board, population_size)
    # evaluate solutions
    boards_and_scores = lamarck_evaluate(board_list, short_input_list, base_board)
    boards_and_scores.sort(key=lambda x: x[1])
    lamarck_best = []
    lamarck_avg = []
    # as long as we dont have a solution
    i = 1
    lam5000 = []
    while (boards_and_scores[0][-1] != 0) & (i < 10000):
        board_list = next_generation(base_board, boards_and_scores, short_input_list)
        # if we didn't find the result in 5000 rounds- start over
        if i == 5001:
            lam5000 = board_list  # save the boards of the first run
            board_list = create_first_generation(base_board, population_size)
        boards_and_scores = lamarck_evaluate(board_list, short_input_list, base_board)
        boards_and_scores.sort(key=lambda x: x[1])
        if i % 100 == 0:
            mean = np.mean([x[1] for x in boards_and_scores])
            print(
                f"best scores of round {i} are: {boards_and_scores[0][-1]}, {boards_and_scores[1][-1]}, {boards_and_scores[2][-1]}")
            print(f"The avg of the scores is {mean}")
            lamarck_best.append(boards_and_scores[0][-1])
            lamarck_avg.append(mean)
        i += 1
    if boards_and_scores[0][-1] == 0:
        print(f"Successssssss!! you're the queen of the world!!! and it only took you like {i} rounds! Crazyyy")
    lamarck_best_board = copy.deepcopy(boards_and_scores[0][0])
    lamarck_best_fitness = boards_and_scores[0][-1]
    lamarck_generations = i
    # if we didn't find a solution- take best board from either last run or run 5000
    if lamarck_generations == 10000:
        boards_and_scores5000 = evaluate(lam5000, short_input_list)
        boards_and_scores5000.sort(key=lambda x: x[1])
        # if the best board is from run 5000
        if boards_and_scores5000[0][-1] < lamarck_best_fitness:
            lamarck_best_board = copy.deepcopy(boards_and_scores5000[0][0])
            lamarck_best_fitness = boards_and_scores5000[0][-1]
    mean = np.mean([x[1] for x in boards_and_scores])
    lamarck_best.append(boards_and_scores[0][-1])
    lamarck_avg.append(mean)

    ### darwinian optimization
    print("\nRunning Darwin algorithm: ")
    # create first generation of solutions
    board_list = create_first_generation(base_board, population_size)
    # evaluate solutions- ng is gor the next generation, real is the real boards scores
    ng_boards_and_scores, real_boards_and_scores = darwinian_evaluate(board_list, short_input_list, base_board)
    ng_boards_and_scores.sort(key=lambda x: x[1])
    real_boards_and_scores.sort(key=lambda x: x[1])
    darwin_best = []
    darwin_avg = []
    # as long as we dont have a solution
    i = 1
    dar5000 = []
    while (real_boards_and_scores[0][-1] != 0) & (i < 10000):
        board_list = next_generation(base_board, ng_boards_and_scores, short_input_list)
        # if we didn't find the result in 5000 rounds- start over
        if i == 5001:
            dar5000 = board_list  # save the boards of the first run
            board_list = create_first_generation(base_board, population_size)
        ng_boards_and_scores, real_boards_and_scores = darwinian_evaluate(board_list, short_input_list, base_board)
        ng_boards_and_scores.sort(key=lambda x: x[1])
        real_boards_and_scores.sort(key=lambda x: x[1])
        if i % 100 == 0:
            mean = np.mean([x[1] for x in real_boards_and_scores])
            print(
                f"best scores of round {i} are: {real_boards_and_scores[0][-1]}, {real_boards_and_scores[1][-1]}, "
                f"{real_boards_and_scores[2][-1]}")
            print(f"The avg of the scores is {mean}")
            darwin_best.append(real_boards_and_scores[0][-1])
            darwin_avg.append(mean)
        i += 1
    if real_boards_and_scores[0][-1] == 0:
        print(f"Successssssss!! you're the queen of the world!!! and it only took you like {i} rounds! Crazyyy")
    darwin_best_board = copy.deepcopy(real_boards_and_scores[0][0])
    darwin_best_fitness = real_boards_and_scores[0][-1]
    darwin_generations = i
    # if we didn't find a solution- take best board from either last run or run 5000
    if darwin_generations == 10000:
        boards_and_scores5000 = evaluate(dar5000, short_input_list)
        boards_and_scores5000.sort(key=lambda x: x[1])
        # if the best board is from run 5000
        if boards_and_scores5000[0][-1] < darwin_best_fitness:
            darwin_best_board = copy.deepcopy(boards_and_scores5000[0][0])
            darwin_best_fitness = boards_and_scores5000[0][-1]
    mean = np.mean([x[1] for x in real_boards_and_scores])
    darwin_best.append(real_boards_and_scores[0][-1])
    darwin_avg.append(mean)

    # displaying best boards and plots
    title = "Regular Algorithm- Best Board"
    print_board(regular_best_board, short_input_list, title, regular_best_fitness, regular_avg[-1], regular_generations)
    plot_plots("Regular Algorithm", regular_best, regular_avg)

    title = "Lamarck Algorithm- Best Board"
    print_board(lamarck_best_board, short_input_list, title, lamarck_best_fitness, lamarck_avg[-1], lamarck_generations)
    plot_plots("Lamarck Algorithm", lamarck_best, lamarck_avg)

    title = "Darwin Algorithm- Best Board"
    print_board(darwin_best_board, short_input_list, title, darwin_best_fitness, darwin_avg[-1], darwin_generations)
    plot_plots("Darwin Algorithm", darwin_best, darwin_avg)

    print("Program Done.")


if __name__ == '__main__':
    main()
