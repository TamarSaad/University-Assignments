import subprocess
import pkg_resources
import sys
import os

# check if the packages being used are installed and if not- install
packages = {'matplotlib', 'numpy', 'pygame', 'easygui'}
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
from itertools import product
from random import sample
import pygame
from easygui import multenterbox

n = 28000  # around 70% of automaton is initialized
d = int(0.01 * n)  # 0.01 of the population
r = int(0.05 * n)  # fast people
x = 6  # generations for being sick and contagious
t = 0.1  # threshold percentage of sick people above it the p value changes
p_big = 0.8  # possibility to infect neighbors when sick percentage is below T
p_small = 0.05  # possibility to infect neighbors when sick percentage is above T
mat_size = 200
total_per_sick = []
sick_number = []
# Colors to use in simulation
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)
white = (255, 255, 255)
black = (0, 0, 0)


def initialize(mat):
    # create a nX2 array of random values for the people
    n_loc = sample(list(product(range(200), repeat=2)), k=n)
    # create a dX2 array of random values for the sick people
    d_loc = sample(n_loc, k=d)
    # create a rX2 array of random values for the fast people
    r_loc = sample(n_loc, k=r)
    # initialize the attributes
    for loc in n_loc:
        if loc in d_loc:
            mat[loc][0] = 'S'
            mat[loc][1] = 1
        else:
            mat[loc][0] = 'H'
        if loc in r_loc:
            mat[loc][2] = True
    return mat


def neighbours_infection(mat, infected_mat, row, col, p, sick_counter):
    # get the locations of the neighbors
    neighbors_row = range((row - 1), (row + 2))
    neighbors_col = range((col - 1), (col + 2))
    # iterate through neighbours
    for nr in neighbors_row:
        for nc in neighbors_col:
            # use modulo for "wrap around" effect
            nrow = nr % mat_size
            ncol = nc % mat_size
            # if the neighbour is healthy- try to infect it with probability p
            if infected_mat[nrow][ncol][0] == 'H':
                if np.random.uniform(0, 1) <= p:
                    infected_mat[nrow][ncol][0] = 'S'
                    infected_mat[nrow][ncol][1] = str(1)
                    sick_counter += 1
    return infected_mat, sick_counter


def infection(mat, sick_counter):
    # % of sick people
    per_sick = (sick_counter / n)
    total_per_sick.append(per_sick * 100)
    sick_number.append(sick_counter)
    # define the probability for infection
    if per_sick >= t:
        p = p_small
    else:
        p = p_big
    infected_mat = copy.deepcopy(mat)  # deep copy to the original mat
    # iterate through the matrix
    for row in range(mat_size):
        for col in range(mat_size):
            # if the cell is sick
            if mat[row][col][0] == 'S':
                # raise the counter
                infected_mat[row][col][1] = int(infected_mat[row][col][1]) + 1
                # infect neighbours
                infected_mat, sick_counter = neighbours_infection(mat, infected_mat, row, col, p, sick_counter)
                # if the cell was sick long enough it will become "recovered"
                if infected_mat[row][col][1] == str(x):
                    infected_mat[row][col][0] = 'R'
                    sick_counter -= 1
    # print(sick_counter)
    return infected_mat, sick_counter


"""
explanation for movement:
We chose to implement the movement of people in the system by using the current matrix and the future movement matrix. 
To prevent from two people to be in the same cell in the next generation we created the function - "find_free_locations"
Whose job it is to find and return all the available and allowed cells for that person. 
First the function keeps the current position for that person, then goes through the remaining 8 cells and checks if 
they are free in both the current matrix and the future movement matrix, if so, it adds them to the list of free cells.
In this implementation at worst case each cell always has its own location to stay in the next generation.
Then, a random draw in a Uniform distribution is made between the possible free cells, and the selected cell is 
initialized to be the cell of that person in the next generation.
"""


def find_free_locations(mat, move_mat, row, col):
    # list of free locations, initialized with current location
    free_nadlan = [[row, col]]
    # get the locations of the neighbors
    neighbors_row = range((row - 1), (row + 2))
    neighbors_col = range((col - 1), (col + 2))
    # iterate through neighbours
    for nr in neighbors_row:
        for nc in neighbors_col:
            # use modulo for "wrap around" effect
            nrow = nr % mat_size
            ncol = nc % mat_size
            # if the cell is available in both mats - add it to the list
            if move_mat[nrow][ncol][0] == 'E' and mat[nrow][ncol][0] == 'E':
                free_nadlan.append([nrow, ncol])
    return free_nadlan


# movement for fast people
def move_fast(mat, new_mat, row, col):
    # list of free locations, initialized with current location
    free_nadlan = [[row, col]]
    # the options for movement of fast people
    movement_options = [-10, 0, 10]
    # go trough all the different positions
    for height in movement_options:
        for width in movement_options:
            # don't ask me why, but that was my conclusion that will work
            lr = (row + height + mat_size) % mat_size
            lc = (col + width + mat_size) % mat_size
            # if the new location is empty- it's a possible new home
            if new_mat[lr][lc][0] == 'E' and mat[lr][lc][0] == 'E':
                free_nadlan.append([lr, lc])
    return free_nadlan


# # if there are collisions in the movement matrix
# def fix_collision(row, col, move_mat, old_mat):
#     # save the old cell
#     cell = old_mat[row][col]
#     while True:
#         # define the locations for the bottom right cell in a wrap around way
#         wrap_row = (row + 1) % mat_size
#         wrap_col = (col + 1) % mat_size
#         # save the current cell that in the bottom right
#         temp_cell = move_mat[wrap_row, wrap_col]
#         # put the current cell in the new matrix in the bottom right instead
#         move_mat[wrap_row, wrap_col] = cell
#         # find the available locations for that cell and move it
#         free_nadlan = find_free_locations(old_mat, move_mat, wrap_row, wrap_col)
#         row += 1
#         col += 1
#         cell = temp_cell
#         # if we found free space for the new cell- break
#         if len(free_nadlan) != 0:
#             break
#     new_home = random.choice(free_nadlan)
#     move_mat[new_home[0]][new_home[1]] = cell
#     return move_mat


def movement(mat):
    # initialize a new matrix
    cell = ['E', 0, False]
    move_mat = np.full((200, 200, 3), cell)
    # iterate through the original matrix
    for row in range(mat_size):
        for col in range(mat_size):
            # if there's someone in the cell
            if mat[row][col][0] != 'E':
                # if the person is fast
                if mat[row][col][2] == True:
                    free_nadlan = move_fast(mat, move_mat, row, col)
                else:
                    # define the available locations for him to move
                    free_nadlan = find_free_locations(mat, move_mat, row, col)
                # if there are no free locations, there is always the current location
                new_home = random.choice(free_nadlan)
                move_mat[new_home[0]][new_home[1]] = mat[row][col]
    return move_mat


# if one of the user inputs is not by the orders- the default parameters will be used
def input_check(parameters):
    flag = True
    if len(parameters) < 7:
        print("num args")
        flag = False
    else:
        n_num, d_num, r_num, x_num, t_num, p_big_num, p_small_num = parameters
        if not n_num.isdigit() or int(n_num) <= 0 or int(n_num) > (mat_size * mat_size):
            print("n problem")
            flag = False
        elif float(d_num) < 0 or float(d_num) > 1:
            print("d problem")
            flag = False
        elif float(r_num) < 0 or float(r_num) > 1:
            print("r problem")
            flag = False
        elif not x_num.isdigit() or int(x_num) < 0:
            print("x problem")
            flag = False
        elif float(t_num) < 0 or float(t_num) > 1:
            print("t problem")
            flag = False
        elif float(p_big_num) < 0 or float(p_big_num) > 1:
            print("p_big problem")
            flag = False
        elif float(p_small_num) < 0 or float(p_small_num) > float(p_big_num):
            print("p_small problem")
            flag = False
    if flag:  # user params
        globals()['n'] = int(n_num)  # around 70% of automaton is initialized
        globals()['d'] = int(float(d_num) * n)  # 0.01 of the population
        globals()['r'] = int(float(r_num) * n)  # fast people
        globals()['x'] = int(x_num)  # generations for being sick and contagious
        globals()['t'] = float(t_num)  # threshold percentage of sick people above it the p value changes
        globals()['p_big'] = float(p_big_num)  # possibility to infect neighbors when sick percentage is below T
        globals()['p_small'] = float(p_small_num)  # possibility to infect neighbors when sick percentage is above T
    return flag


# Function to create a button on the pygame screen
def create_button(x, y, width, height, hovercolor, defaultcolor, screen):
    mouse = pygame.mouse.get_pos()
    # Mouse get pressed can run without an integer, but needs a 3 or 5 to indicate how many buttons
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))


def show_params(screen):
    # create text for display
    # font
    font = pygame.font.SysFont('comicsansms', 12)
    parameters_txt = font.render(
        f'Simulation params: N={n}, D={d}, R={r}, T={t}, X={x}, p_big={p_big}, p_small={p_small}'
        , True, slategrey)
    # show text (image variable,(left, top))
    screen.blit(parameters_txt, (5, 0))

    if len(total_per_sick) > 0:
        sick_percentage_txt = font.render("sick_percentage=" + str(total_per_sick[-1]), True, blackish)
        screen.blit(sick_percentage_txt, (5, parameters_txt.get_height()))


def main():
    # getting the user input for the simulation
    # window title
    title = "Covid19 Automaton simulation parameters"
    # informing the user which are the default params
    text = "Presented to you are the default parameters. you can alter them if you want"
    # inputs fields
    inputs = ["Number of people in the system-N (0-40,000)", "Percentage of initial sick people-D (0-1)",
              "Percentage of fast people-R (0-1)", "Number of sickness generations-X (integer)",
              "Threshold value-T (0-1)", "Probability of infection when sick percentage is below T-P_BIG (0-1)",
              "Probability of infection when sick percentage is above T-P_SMALL (0-P_BIG)"]
    # list of default params
    default_params = ["28000", "0.01", "0.05", "6", "0.1", "0.8", "0.05"]

    output = multenterbox(text, title, inputs, default_params)
    if output == default_params:
        print("Default params are being used..")
    else:
        flag = input_check(output)
        if flag is False:
            print("Wrong input, Default params are being used..")
        else:
            print("user parameters are being used")

    ####### initialize
    # every cell has 3 attributes: state, number of generations as sick and binary value of R
    cell = ['E', 0, False]
    mat = np.full((200, 200, 3), cell)
    mat = initialize(mat)
    sick_counter = d
    generation = 1

    # Initialize pygame
    width = 600
    height = 640
    # initialize game
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Covid19 Simulation")
    # setting clock
    clock = pygame.time.Clock()

    # Game loop
    running = True
    game_running = True
    while running:
        # white color for the screen
        screen.fill(white)
        show_params(screen)

        # start button (left, top, width, height)
        start_button = create_button(width - 120, 7, 110, 26, lightgrey, slategrey, screen)
        # if start button was pressed
        if start_button:
            while game_running:
                screen.fill(white)
                show_params(screen)
                # iterate through the original matrix
                for row in range(mat_size):
                    for col in range(mat_size):
                        # if there's someone in the cell
                        # calc rec size for filling
                        rect = (row * 3, col * 3 + 40, width / mat_size, width / mat_size)
                        # check status and choose the right color
                        if mat[row][col][0] == 'S':
                            screen.fill((255, 0, 0), rect=rect)  # red
                        if mat[row][col][0] == 'H':
                            screen.fill((0, 255, 0), rect=rect)  # green
                        if mat[row][col][0] == 'R':
                            screen.fill(black, rect=rect)  # black

                # update
                mat, sick_counter = infection(mat, sick_counter)
                mat = movement(mat)
                generation += 1

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_running = False

                pygame.display.update()
                clock.tick(30)

                # stop pygame when no more sick people
                if sick_counter <= 0:
                    game_running = False

        # start button text
        # font
        font = pygame.font.SysFont('comicsansms', 12)
        startbuttontext = font.render("Start Simulation", True, blackish)
        screen.blit(startbuttontext, (width - 115, 9))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()
        clock.tick(30)

        # if the simulation finished running we end the main loop to
        if not game_running:
            running = False
    # create a plot only if the simulation was played
    if not game_running:
        plt.plot(range(1, generation), total_per_sick)
        plt.xlabel('Generations')
        plt.ylabel('Percentage of Sick')
        plt.title(f'N = {n}, D = {d}, R = {r}, T = {t}\n X = {x}, p_big = {p_big}, p_small = {p_small} ')
        plt.show()


if __name__ == '__main__':
    main()
