#!/usr/bin/env python

# This module decides when the genetic algorithm should stop. 
# Currently, we only use a maximum number of generations as the stopping criterion.

from src import config

def shouldTerminate(population, gen):
    """
    Determines if the genetic algorithm should stop.
    :param population: List of individuals in the population.
    :param gen: Current generation number.
    :return: True if the generation number exceeds the maximum allowed, otherwise False.
    """
    return gen > config.maxGen      