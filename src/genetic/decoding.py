#!/usr/bin/env python

import sys

# Objective: Split the ms vector (machine sequence) into sub-sequences for each job.
# Inputs:
# pb_instance: Problem instance containing job details.
# ms: Sequence of machines.
# Output: List of machine sub-sequences for each job.
def split_ms(pb_instance, ms):
    """
    Splits the ms vector (machine sequence) into sub-sequences for each job.
    :param pb_instance: Dictionary containing job details.
    :param ms: List of machines.
    :return: List of machine sub-sequences for each job.
    """
    jobs = []
    current = 0
    for index, job in enumerate(pb_instance['jobs']):
        jobs.append(ms[current:current+len(job)])
        current += len(job)

    return jobs

# Objective: Find the processing time of an operation on a given machine.
# Inputs:
# op_by_machine: List of operations by machine.
# machine_nb: Machine number.
# Output: Processing time of the operation on the specified machine.
def get_processing_time(op_by_machine, machine_nb):
    """
    Finds the processing time of an operation on a given machine.
    :param op_by_machine: List of operations by machine.
    :param machine_nb: Machine number.
    :return: Processing time of the operation on the specified machine.
    """
    for op in op_by_machine:
        if op['machine'] == machine_nb:
            return op['processingTime']
    print("[ERROR] Machine {} doesn't seem to be able to process this task.".format(machine_nb))
    sys.exit(-1)

# Objective: Check if a time interval is free on a machine.
# Inputs:
# tab: Array indicating used time slots.
# start: Start of the interval.
# duration: Duration of the interval.
# Output: True if the interval is free, False otherwise.
def is_free(tab, start, duration):
    """
    Checks if a time interval is free on a machine.
    :param tab: Array indicating used time slots.
    :param start: Start of the interval.
    :param duration: Duration of the interval.
    :return: True if the interval is free, False otherwise.
    """
    for k in range(start, start+duration):
        if not tab[k]:
            return False
    return True

# Objective: Find the first available time slot for an operation on a machine.
# Inputs:
# start_ctr: Start constraint.
# duration: Operation duration.
# machine_jobs: List of operations on the machine.
# Output: First available time for the operation.
def find_first_available_place(start_ctr, duration, machine_jobs):
    """
    Finds the first available time slot for an operation on a machine.
    :param start_ctr: Start constraint.
    :param duration: Operation duration.
    :param machine_jobs: List of operations on the machine.
    :return: First available time for the operation.
    """
    max_duration_list = []
    max_duration = start_ctr + duration

    # max_duration is either start_ctr + duration or the max(possible starts) + duration
    if machine_jobs:
        for job in machine_jobs:
            max_duration_list.append(job[3] + job[1])  # start + processing time

        max_duration = max(max(max_duration_list), start_ctr) + duration

    machine_used = [True] * max_duration

    # Update the array with the used time slots
    for job in machine_jobs:
        start = job[3]
        long = job[1]
        for k in range(start, start + long):
            machine_used[k] = False

    # Find the first available time interval that satisfies the constraint
    for k in range(start_ctr, len(machine_used)):
        if is_free(machine_used, k, duration):
            return k

# Objective: Decode the operation sequence (os) and machine sequence (ms) into a detailed production schedule.
# Inputs:
# pb_instance: Problem instance.
# os: Operation sequence.
# ms: Machine sequence.
# Output: List of scheduled operations for each machine.
def decode(pb_instance, os, ms):
    """
    Decodes the operation sequence (os) and machine sequence (ms) into a detailed production schedule.
    :param pb_instance: Problem instance.
    :param os: Operation sequence.
    :param ms: Machine sequence.
    :return: List of scheduled operations for each machine.
    """
    o = pb_instance['jobs']
    machine_operations = [[] for i in range(pb_instance['machinesNb'])]

    ms_s = split_ms(pb_instance, ms)  # machine for each operation

    indexes = [0] * len(ms_s)
    start_task_cstr = [0] * len(ms_s)

    # Iterate over OS to get task execution order and look up MS for the machine
    for job in os:
        index_machine = ms_s[job][indexes[job]]
        machine = o[job][indexes[job]][index_machine]['machine']
        prcTime = o[job][indexes[job]][index_machine]['processingTime']
        start_cstr = start_task_cstr[job]

        # Get the first available time interval for the operation
        start = find_first_available_place(start_cstr, prcTime, machine_operations[machine - 1])
        name_task = "OP_{}-{}".format(job + 1, indexes[job] + 1)

        machine_operations[machine - 1].append((name_task, prcTime, start_cstr, start))

        # Update indexes (one for the current task of each job, one for the start constraint of each job)
        indexes[job] += 1
        start_task_cstr[job] = (start + prcTime)

    return machine_operations


# Objective: Convert scheduled operations into a format usable for Gantt chart generation.
# Inputs:
# machine_operations: List of scheduled operations per machine.
# Output: Dictionary formatted for a Gantt chart.
def translate_decoded_to_gantt(machine_operations):
    """
    Converts scheduled operations into a format usable for Gantt chart generation.
    :param machine_operations: List of scheduled operations per machine.
    :return: Dictionary formatted for a Gantt chart.
    """
    data = {}

    for idx, machine in enumerate(machine_operations):

        machine_name = "Machine-{}".format(idx + 1)

        operations = []
        for operation in machine:
            operations.append([operation[3], operation[3] + operation[1], operation[0]])
        operations
        data[machine_name] = operations

    return data
