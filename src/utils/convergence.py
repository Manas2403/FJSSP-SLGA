import matplotlib.pyplot as plt  # Import for plotting
import os

def plot_convergence(steps, output_folder):
    """
    Generates a convergence plot showing the evolution of the best and average fitness (makespan)
    over the generations.
    """
    generations = [step['generation'] for step in steps]
    best_times = [step['best_time'] for step in steps]
    average_times = [step['average_time'] for step in steps]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, best_times, marker='o', label='Best Fitness (Makespan)')
    plt.plot(generations, average_times, marker='x', label='Average Fitness (Makespan)')
    plt.xlabel('Generation')
    plt.ylabel('Fitness (Makespan Time)')
    plt.title('Convergence Behavior: Best vs Average Fitness')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_folder, "convergence_plot.png"))
    plt.close()
    print(f"Convergence plot saved in '{output_folder}'.")