import matplotlib.pyplot as plt  # Import for plotting
import os

def plot_parameter_adaptation(steps, output_folder):
    """
    Generates a plot showing how the crossover probability (Pc) and mutation probability (Pm)
    are adapted over the generations.
    """
    generations = [step['generation'] for step in steps]
    pc_values = [step['Pc'] for step in steps]
    pm_values = [step['Pm'] for step in steps]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, pc_values, marker='o', label='Crossover Rate (Pc)')
    plt.plot(generations, pm_values, marker='x', label='Mutation Rate (Pm)')
    plt.xlabel('Generation')
    plt.ylabel('Probability')
    plt.title('Parameter Adaptation: Pc and Pm vs. Generation')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_folder, "parameter_adaptation.png"))
    plt.close()
    print(f"Parameter adaptation plot saved in '{output_folder}'.")