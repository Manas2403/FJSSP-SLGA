#!/usr/bin/env python

# This module creates a population of random OS and MS chromosomes.

import random
from src import config

def generateOS(parameters):
    """
    Generates a random OS chromosome (Operation Sequence Order) for the jobs.
    :param parameters: Dictionary containing job information.
    :return: List representing the OS chromosome.
    """
    jobs = parameters['jobs']

    OS = []
    i = 0
    for job in jobs:
        for op in job:
            OS.append(i)
        i = i + 1
    # Random shuffle of the OS chromosome elements
    random.shuffle(OS)

    return OS

def generateMS(parameters):
    """
    Generates a random MS chromosome (Machine Selection) for the jobs.
    :param parameters: Dictionary containing job information.
    :return: List representing the MS chromosome.
    """
    jobs = parameters['jobs']
    MS = []
    for job in jobs:
        for op in job:
            # Randomly select a machine for each operation
            randomMachine = random.randint(0, len(op) - 1)
            MS.append(randomMachine)
        
    return MS

def initializePopulation(parameters):
    """
    Initializes the population with random OS and MS chromosomes.
    :param parameters: Dictionary containing job information.
    :return: List of tuples representing the initial population of chromosomes (OS, MS).
    """
    gen1 = []

    for i in range(config.popSize):
        OS = generateOS(parameters)
        MS = generateMS(parameters)
        gen1.append((OS, MS))

    return gen1
