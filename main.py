import numpy as np
from random import shuffle, sample
from random import randrange

N_GENERATIONS = 10
CHROMOSOMES = 4


def read_input_file():
    with open('input.txt') as f:
        return f.read().splitlines()


def init_passengers_seats(dims, passengers_list):
    aircraft = initialize_aircraft(dims)
    shuffle(passengers_list)  # we want different configurations to create different chromosomes

    i = int(0)
    j = int(0)

    for a in passengers_list:
        passengers_group = a.split(' ')
        group_id = '_' + str(randrange(99))
        for passenger in passengers_group:
            if j == 4:
                j = 0
                i += 1
            aircraft[i, j] = passenger + group_id  # we hope no collision
            j += 1

    return aircraft


# A new aircraft(gen) with 0's
def initialize_aircraft(dims):
    aircraft = np.chararray(shape=(int(dims[0]), int(dims[1])), itemsize=6)
    aircraft[:] = '0'
    return aircraft


def initialize_passenger_list(input_lines):
    passengers_list = []
    for l in input_lines[1:]:
        passengers_list.append(l)
    return passengers_list


def initialize_chromosome(dims, passengers_list):
    #     import pdb; pdb.set_trace()
    chromosome = []
    for i in range(4):
        chromosome.append(init_passengers_seats(dims, passengers_list))
    return chromosome


def initialize_population(num_chromosomes, dims, passengers_list):
    init_population = []
    for i in range(num_chromosomes):
        init_population.append(initialize_chromosome(dims, passengers_list))
    return init_population


def fitness(aircraft):
    total_window_miss = window_miss_allocated(aircraft)
    total_group_miss = group_seat_miss(aircraft)
    return 100 - (total_window_miss + total_group_miss / (aircraft.shape[0] * aircraft.shape[1]) * 100)


# Look into passengers that want window but are seated in the middle
def window_miss_allocated(aircraft):
    window_miss = 0
    for i in range(0, 4):
        for j in range(1, 3):
            if 'w' in str(aircraft[i, j]):
                window_miss += 1
    return window_miss


def group_seat_miss(passengers):
    seat_miss = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if (look_left(i, j, passengers) < 0 or look_right(i, j, passengers) < 0) \
                    and search_same_group(i, j, passengers) != 0:
                seat_miss += 1
    return seat_miss


def select_breed(population, num_chromosomes, crossover_info):
    print('selecting breed...')
    if len(crossover_info) == 0:
        for i in range(num_chromosomes):
            crossover_info['bestGenPosition_' + str(i)] = 0
            crossover_info['worstGenPosition_' + str(i)] = 0

    crossover_info['bestGen'] = 0
    crossover_info['bestFitness'] = 0

    best_fitness = 0
    worst_fitness = 0
    cross_over_index = 1
    for chromosome in population:
        gen_position = 0
        for gen in chromosome:
            gen_fitness = fitness(gen)
            # select best and worst to crossover
            if gen_fitness > best_fitness:
                best_fitness = gen_fitness
                crossover_info["bestGenPosition_" + str(cross_over_index)] = gen_position
                crossover_info["bestFitness"] = best_fitness
                crossover_info['bestGen'] = gen
            if gen_fitness < worst_fitness:
                crossover_info["worstGenPosition_" + str(cross_over_index)] = gen_position

            gen_position += 1
        cross_over_index += 1

    return crossover_info


def crossover(gen_info, population):
    print('crossover')
    i = 0
    while i < len(population):
        population[i][gen_info['worstGenPosition_' + str(i)]] = population[i + 1][
            gen_info['bestGenPosition_' + str(i + 1)]]
        mutate(population[i][gen_info['worstGenPosition_' + str(i)]])
        population[i + 1][gen_info['worstGenPosition_' + str(i + 1)]] = population[i][
            gen_info['bestGenPosition_' + str(i)]]
        mutate(population[i + 1][gen_info['worstGenPosition_' + str(i + 1)]])
        i = i + 2
    return population


# Mutation prob is 3%
def mutate(gen):
    if randrange(100) <= 3:
        print('apply mutation!!')
        swap_position_1 = [0, 0]
        swap_position_2 = [0, 0]
        while swap_position_1 == swap_position_2:
            swap_position_1 = get_swap_position()
            swap_position_2 = get_swap_position()

        passenger_to_swap = gen[swap_position_2[0]][swap_position_2[1]]

        gen[swap_position_2[0]][swap_position_2[1]] = gen[swap_position_1[0]][swap_position_1[1]]
        gen[swap_position_1[0]][swap_position_1[1]] = passenger_to_swap
    return gen


def get_swap_position():
    return sample([0, 1, 2, 3], k=2)


def look_left(i, j, aircraft):
    if j > 0:
        passenger = str(aircraft[i, j]).split('_')[1]
        if passenger not in str(aircraft[i, j - 1]).split('_')[1]:
            return -1
    return 0


def look_right(i, j, aircraft):
    if j < 3:
        passenger = str(aircraft[i, j]).split('_')[1]
        if passenger not in str(aircraft[i, j + 1]).split('_')[1]:
            return -1
    return 0


def reorder_passengers(chromosome):
    for i in range(0, 4):
        gen = chromosome[i].copy()
        for row in range(0, 4):
            for col in range(0, 4):
                if look_left(row, col, gen) < 0 or look_right(row, col, gen) < 0:
                    reallocate_passenger(gen, row, col)
    chromosome[i] = gen
    return chromosome


def reallocate_passenger(gen, row, col):
    same_group_position = search_same_group(row, col, gen)
    if (same_group_position != 0 and look_left(row, col, gen) == 0 and col >= 1
        and not is_window(gen[same_group_position[0]][same_group_position[1] - 1])):
        aux = gen[same_group_position[0]][same_group_position[1] - 1]
        gen[same_group_position[0]][same_group_position[1] - 1] = gen[row][col]
        gen[row][col] = aux
    elif (same_group_position != 0 and look_right(row, col, gen) == 0 and same_group_position[1] <= 2
        and not is_window(gen[same_group_position[0]][same_group_position[1] + 1])):
        aux = gen[same_group_position[0]][same_group_position[1] + 1]
        gen[same_group_position[0]][same_group_position[1] + 1] = gen[row][col]
        gen[row][col] = aux
    return gen


def is_window(seat):
    if "w" not in str(seat).split('_')[0]:
        return True
    else:
        return False


def search_same_group(row, col, gen):
    for i in range(0, 4):
        for j in range(0, 4):
            if row != i and col != j and str(gen[i][j]).split('_')[1] == str(gen[row][col]).split('_')[1]:
                return i, j
    return 0


def main():
    input = read_input_file()
    passengers_list = initialize_passenger_list(input)
    aircraft_dims = input[0].split(' ')

    # Init population
    population = initialize_population(CHROMOSOMES, aircraft_dims, passengers_list)
    crossover_info = {}

    print("Starting GA...")
    for _ in range(N_GENERATIONS):
        print('generation:', _)
        for i in range(CHROMOSOMES):
            population[i] = reorder_passengers(population[i])

        select_breed(population, CHROMOSOMES, crossover_info)
        crossover(crossover_info, population)

    print('\n === satisfaction: ' + str(crossover_info['bestFitness']))
    print(' === best aircraft configuration (gen) \n\n' + str(crossover_info['bestGen']))


if __name__ == '__main__':
    main()
