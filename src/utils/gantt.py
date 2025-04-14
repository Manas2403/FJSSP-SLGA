#!/usr/bin/env python

# This module helps create Gantt charts from a dictionary.
# The output format is a Matplotlib plot.

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import colors as mcolors


# Function to generate a list of random colors
def generate_colors(n):
    """
    Generates n distinct colors ensuring no repetitions.
    :param n: Number of colors to generate.
    :return: List of RGB colors.
    """
    print("Generating color n:", n)
    base_colors = list(mcolors.CSS4_COLORS.values())  # Use CSS4 colors for diversity
    random.shuffle(base_colors)  # Shuffle base colors for randomness
    colors = []
    print("Start loop")

    # Add base colors until the required number is reached or all are used
    for color in base_colors:
        if len(colors) >= n:
            break
        rgb_color = mcolors.to_rgb(color)
        if rgb_color not in colors:
            colors.append(rgb_color)

    # If number of jobs exceeds available colors, generate additional ones
    while len(colors) < n:
        colors.append(mcolors.hsv_to_rgb([random.random(), 0.5 + 0.5 * random.random(), 1.0]))
    
    return colors


# Function to draw the Gantt chart
def draw_chart(data, filename='gantt.svg'):
    """
    Draws a Gantt chart and saves it as an SVG file.
    :param data: Dictionary containing scheduled operations per machine.
    :param filename: Name of the output SVG file.
    """
    nb_row = len(data.keys())  # Number of machines (rows in the chart)
    nb_jobs = sum(len(machine) for machine in data.values())  # Total number of jobs

    # Dictionary to store assigned colors per job
    job_colors = {}

    # Generate additional colors if many jobs exist
    additional_colors = generate_colors(nb_jobs)
    # Positions of bars on the y-axis with more spacing to prevent overlap
    pos = np.arange(0.5, nb_row * 1.0 + 0.5, 1.0)

    fig = plt.figure(figsize=(20, 12))  # Increase figure size for better spacing
    ax = fig.add_subplot(111)

    index = 0
    max_len = []  # List to store operation end times
    for machine, operations in sorted(data.items()):
        for op in operations:
            max_len.append(op[1])  # Add operation end time to max_len
            job = op[2].split('-')[0]  # Extract job ID
            if job not in job_colors:
                # Assign a new color if the job doesn't have one
                job_colors[job] = additional_colors[len(job_colors) % len(additional_colors)]
            c = job_colors[job]  # Get the color assigned to the job
            rect = ax.barh((index * 1.0) + 0.5, op[1] - op[0], left=op[0], height=0.4, align='center',
                           edgecolor=c, color=c, alpha=0.8)

            # Add label
            width = int(rect[0].get_width())
            Str = "{}".format(op[2])  # Label text (operation name)
            xloc = op[0] + 0.50 * width  # x-position of label
            clr = 'black'  # Label color
            align = 'center'  # Label alignment

            yloc = rect[0].get_y() + rect[0].get_height() / 2.0  # y-position of label
            # Add label with smaller font and vertical orientation
            ax.text(xloc, yloc, Str, horizontalalignment='center',
                    verticalalignment='center', color=clr, weight='bold',
                    clip_on=True, fontsize=8, rotation=90)

        index += 1

    # Set y-axis limits
    ax.set_ylim(ymin=-0.1, ymax=nb_row * 1.0 + 0.5)
    # Add grid
    ax.grid(color='gray', linestyle=':')
    # Set x-axis limits
    ax.set_xlim(0, max(10, max(max_len)))

    # Rotate x-axis labels
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=0, fontsize=10)

    # Set y-axis labels
    locsy, labelsy = plt.yticks(pos, data.keys())
    plt.setp(labelsy, fontsize=14)

    # Set legend properties
    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    # Invert y-axis
    ax.invert_yaxis()

    # Add total makespan to title
    total_makespan = max(max_len)
    plt.title(f"Flexible Job Shop Solution GA Native (Makespan: {total_makespan})")

    # Save Gantt chart
    plt.savefig(filename)
    # Close figure to avoid displaying it
    plt.close(fig)
