#!/usr/bin/env python

# This module contains the detailed implementation of each genetic operator.
# The code strictly follows section 4.3 of the provided paper.

import random
import itertools
from src import config
from src.genetic import decoding

# Objective: Compute the total time needed to execute a set of operations and machines.
# Inputs:
#     os_ms: A tuple containing the operation sequence (os) and machine sequence (ms).
#     pb_instance: The problem instance.
# Output: The maximum time required by any machine.
def timeTaken(os_ms, pb_instance):
    """
    Computes the total time needed to execute a set of operations and machines.
    :param os_ms: Tuple containing the operation sequence (os) and machine sequence (ms).
    :param pb_instance: Dictionary containing job details.
    :return: The maximum time required by any machine.
    """
    (os, ms) = os_ms
    decoded = decoding.decode(pb_instance, os, ms)

    # Get the maximum end time per machine
    max_per_machine = []
    for machine in decoded:
        max_d = 0
        for job in machine:
            end = job[3] + job[1]
            if end > max_d:
                max_d = end
        max_per_machine.append(max_d)

    return max(max_per_machine)


# 4.3.1 Selection
#######################
# Objective: Select the best individuals from the population.
# Details: Sorts the population by time taken and keeps a percentage (pr) of the best individuals.
def elitistSelection(population, parameters):
    """
    Selects the best individuals from the population.
    :param population: List of individuals in the population.
    :param parameters: Dictionary containing job details.
    :return: List of selected best individuals.
    """
    keptPopSize = int(config.pr * len(population))
    sortedPop = sorted(population, key=lambda cpl: timeTaken(cpl, parameters))
    return sortedPop[:keptPopSize]

def tournamentSelection(population, parameters):
    """
    Selects individuals using tournament selection.
    :param population: List of individuals in the population.
    :param parameters: Dictionary containing job details.
    :return: Selected individual.
    """
    b = 2

    selectedIndividuals = []
    for i in range(b):
        randomIndividual = random.randint(0, len(population) - 1)
        selectedIndividuals.append(population[randomIndividual])

    return min(selectedIndividuals, key=lambda cpl: timeTaken(cpl, parameters))

def selection(population, parameters):
    """
    Selects individuals for the new population.
    :param population: List of individuals in the population.
    :param parameters: Dictionary containing job details.
    :return: New selected population.
    """
    newPop = elitistSelection(population, parameters)
    while len(newPop) < len(population):
        newPop.append(tournamentSelection(population, parameters))

    return newPop


# 4.3.2 Crossover Operators
###########################

def precedenceOperationCrossover(p1, p2, parameters):
    """
    Precedence-based operation crossover operator.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionary containing job details.
    :return: Tuple of offspring (o1, o2).
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(1, jobNumber+1)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
        else:
            o1.append(-1)
            p1kept.append(e)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset1:
            o2.append(e)
        else:
            o2.append(-1)
            p2kept.append(e)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def jobBasedCrossover(p1, p2, parameters):
    """
    Job-based crossover operator.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionary containing job details.
    :return: Tuple of offspring (o1, o2).
    """
    J = parameters['jobs']
    jobNumber = len(J)
    jobsRange = range(0, jobNumber)
    sizeJobset1 = random.randint(0, jobNumber)

    jobset1 = random.sample(jobsRange, sizeJobset1)
    jobset2 = [item for item in jobsRange if item not in jobset1]

    o1 = []
    p1kept = []
    for i in range(len(p1)):
        e = p1[i]
        if e in jobset1:
            o1.append(e)
            p1kept.append(e)
        else:
            o1.append(-1)

    o2 = []
    p2kept = []
    for i in range(len(p2)):
        e = p2[i]
        if e in jobset2:
            o2.append(e)
            p2kept.append(e)
        else:
            o2.append(-1)

    for i in range(len(o1)):
        if o1[i] == -1:
            o1[i] = p2kept.pop(0)

    for i in range(len(o2)):
        if o2[i] == -1:
            o2[i] = p1kept.pop(0)

    return (o1, o2)

def twoPointCrossover(p1, p2):
    """
    Two-point crossover operator.
    :param p1: Parent 1.
    :param p2: Parent 2.
    :return: Tuple of offspring (offspring1, offspring2).
    """
    pos1 = random.randint(0, len(p1) - 1)
    pos2 = random.randint(0, len(p1) - 1)

    if pos1 > pos2:
        pos2, pos1 = pos1, pos2

    offspring1 = p1
    if pos1 != pos2:
        offspring1 = p1[:pos1] + p2[pos1:pos2] + p1[pos2:]

    offspring2 = p2
    if pos1 != pos2:
        offspring2 = p2[:pos1] + p1[pos1:pos2] + p2[pos2:]

    return (offspring1, offspring2)

def crossoverOS(p1, p2, parameters):
    """
    Applies crossover on operation sequences (OS).
    :param p1: Parent 1.
    :param p2: Parent 2.
    :param parameters: Dictionary containing job details.
    :return: Tuple of OS offspring (oOS1, oOS2).
    """
    if random.choice([True, False]):
        return precedenceOperationCrossover(p1, p2, parameters)
    else:
        return jobBasedCrossover(p1, p2, parameters)

def crossoverMS(p1, p2):
    """
    Applies two-point crossover on machine sequences (MS).
    :param p1: Parent 1.
    :param p2: Parent 2.
    :return: Tuple of MS offspring (oMS1, oMS2).
    """
    return twoPointCrossover(p1, p2)

def crossover(population, parameters, pc):
    """
    Applies crossover on the entire population.
    :param population: List of individuals.
    :param parameters: Dictionary containing job details.
    :return: New population after crossover.
    """
    newPop = []
    i = 0
    while i < len(population):
        (OS1, MS1) = population[i]
        (OS2, MS2) = population[i+1]

        if random.random() < pc:
            (oOS1, oOS2) = crossoverOS(OS1, OS2, parameters)
            (oMS1, oMS2) = crossoverMS(MS1, MS2)
            newPop.append((oOS1, oMS1))
            newPop.append((oOS2, oMS2))
        else:
            newPop.append((OS1, MS1))
            newPop.append((OS2, MS2))

        i = i + 2

    return newPop


# 4.3.3 Mutation Operators
##########################

def swappingMutation(p):
    """
    Swapping mutation operator.
    :param p: Individual to mutate.
    :return: Mutated individual.
    """
    pos1 = random.randint(0, len(p) - 1)
    pos2 = random.randint(0, len(p) - 1)

    if pos1 == pos2:
        return p

    if pos1 > pos2:
        pos1, pos2 = pos2, pos1

    offspring = p[:pos1] + [p[pos2]] + \
          p[pos1+1:pos2] + [p[pos1]] + \
          p[pos2+1:]

    return offspring

def neighborhoodMutation(p):
    """
    Neighborhood mutation operator.
    :param p: Individual to mutate.
    :return: Mutated individual.
    """
    pos3 = pos2 = pos1 = random.randint(0, len(p) - 1)

    while p[pos2] == p[pos1]:
        pos2 = random.randint(0, len(p) - 1)

    while p[pos3] == p[pos2] or p[pos3] == p[pos1]:
        pos3 = random.randint(0, len(p) - 1)

    sortedPositions = sorted([pos1, pos2, pos3])
    pos1 = sortedPositions[0]
    pos2 = sortedPositions[1]
    pos3 = sortedPositions[2]

    e1 = p[sortedPositions[0]]
    e2 = p[sortedPositions[1]]
    e3 = p[sortedPositions[2]]

    permutations = list(itertools.permutations([e1, e2, e3]))
    permutation  = random.choice(permutations)

    offspring = p[:pos1] + [permutation[0]] + \
          p[pos1+1:pos2] + [permutation[1]] + \
          p[pos2+1:pos3] + [permutation[2]] + \
          p[pos3+1:]

    return offspring

def halfMutation(p, parameters):
    """
    Half mutation operator.
    :param p: Individual to mutate.
    :param parameters: Dictionary containing job details.
    :return: Mutated individual.
    """
    o = p
    jobs = parameters['jobs']

    size = len(p)
    r = int(size/2)

    positions = random.sample(range(size), r)

    i = 0
    for job in jobs:
        for op in job:
            if i in positions:
                o[i] = random.randint(0, len(op)-1)
            i = i+1

    return o

def mutationOS(p):
    """
    Applies mutation on operation sequences (OS).
    :param p: Individual to mutate.
    :return: Mutated individual.
    """
    if random.choice([True, False]):
        return swappingMutation(p)
    else:
        return neighborhoodMutation(p)

def mutationMS(p, parameters):
    """
    Applies half mutation on machine sequences (MS).
    :param p: Individual to mutate.
    :param parameters: Dictionary containing job details.
    :return: Mutated individual.
    """
    return halfMutation(p, parameters)

def mutation(population, parameters, pm):
    """
    Applies mutation on the entire population.
    :param population: List of individuals.
    :param parameters: Dictionary containing job details.
    :return: New population after mutation.
    """
    newPop = []

    for (OS, MS) in population:
        if random.random() < pm:
            oOS = mutationOS(OS)
            oMS = mutationMS(MS, parameters)
            newPop.append((oOS, oMS))
        else:
            newPop.append((OS, MS))

    return newPop
