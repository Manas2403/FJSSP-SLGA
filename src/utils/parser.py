#!/usr/bin/env python

# This module parses .fjs files as found in the "Monaldo" FJSP dataset.
# More details on this file format can be found in the dataset documentation.

def parse(path):
    """
    Parses a .fjs file and extracts job and machine information.
    :param path: Path to the .fjs file to parse.
    :return: Dictionary containing the number of machines and job details.
    """
    file = open(path, 'r')  # Open the file for reading

    firstLine = file.readline()  # Read the first line of the file
    firstLineValues = list(map(int, firstLine.split()[0:2]))  # Extract the first two integers from the first line

    jobsNb = firstLineValues[0]  # Number of jobs
    machinesNb = firstLineValues[1]  # Number of machines

    jobs = []  # List to store the jobs

    for i in range(jobsNb):
        currentLine = file.readline()  # Read the current line
        currentLineValues = list(map(int, currentLine.split()))  # Convert line values to integers

        operations = []  # List to store operations for the current job

        j = 1
        while j < len(currentLineValues):
            k = currentLineValues[j]  # Number of options for the current operation
            j = j + 1

            operation = []  # List to store machine options for this operation

            for ik in range(k):
                machine = currentLineValues[j]  # Machine number
                j = j + 1
                processingTime = currentLineValues[j]  # Processing time
                j = j + 1

                operation.append({'machine': machine, 'processingTime': processingTime})  # Add machine-time pair

            operations.append(operation)  # Add current operation to the job

        jobs.append(operations)  # Add the job to the list

    file.close()  # Close the file

    return {'machinesNb': machinesNb, 'jobs': jobs}  # Return dictionary with machines and jobs
