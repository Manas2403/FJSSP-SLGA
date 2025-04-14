import os
import time
import csv
import numpy as np
import random
import matplotlib.pyplot as plt  
from src.utils import parser, gantt
from src.genetic import encoding, decoding, genetic, termination
from src import config

def initialize_SLGA_parameters():
    # Initialization of SLGA parameters
    Pc_range = (0.4, 0.9)
    Pm_range = (0.01, 0.21)
    epsilon = 0.1
    alpha = 0.1
    gamma = 0.9
    return Pc_range, Pm_range, epsilon, alpha, gamma

def initialize_Q_table(population_size):
    return np.zeros((population_size, 2))  # Two possible actions: adjust Pc or Pm

def update_Q_sarsa(Q, state, action, reward, next_state, next_action, alpha, gamma):
    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + gamma * Q[next_state][next_action])
    return Q

def update_Q_qlearning(Q, state, action, reward, next_state, alpha, gamma):
    max_Q_next = max(Q[next_state])
    Q[state][action] = (1 - alpha) * Q[state][action] + alpha * (reward + gamma * max_Q_next)
    return Q

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

def plot_reward(steps, output_folder):
    """
    Generates a plot of the reward received by the RL component at each generation.
    Positive values indicate improvements while negative values indicate degradations in the best fitness.
    """
    generations = [step['generation'] for step in steps]
    rewards = [step['reward'] for step in steps]

    plt.figure(figsize=(10, 6))
    plt.plot(generations, rewards, marker='o', color='green', label='Reward')
    plt.xlabel('Generation')
    plt.ylabel('Reward')
    plt.title('Reward vs. Generation')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_folder, "reward_plot.png"))
    plt.close()
    print(f"Reward plot saved in '{output_folder}'.")

def plot_q_table_heatmap(Q, output_folder):
    """
    Generates a heatmap of the Q-table (states x actions).
    Each row represents a state (generations modulo population size)
    and each column represents an action (0: adjust Pc, 1: adjust Pm).
    """
    plt.figure(figsize=(10, 6))
    plt.imshow(Q, aspect="auto", interpolation="nearest")
    plt.title("Q-Table Heatmap")
    plt.xlabel("Actions (0: Pc, 1: Pm)")
    plt.ylabel("State (Generation mod Population Size)")
    plt.colorbar()
    plt.savefig(os.path.join(output_folder, "q_table_heatmap.png"))
    plt.close()
    print(f"Q-Table heatmap saved in '{output_folder}'.")

def run_genetic_algorithm(data_path, output_folder):
    # Early stopping if no improvement after certain generations
    max_no_improvement_generations = 50
    no_improvement_count = 0
    previous_best_time = float('inf')  # Start with a very high value
    print("Initial max no-improvement generations:", max_no_improvement_generations)
    print("_" * 30)

    # Initialize parameters for each test
    Pc_range, Pm_range, epsilon, alpha, gamma = initialize_SLGA_parameters()
    print("Pc range:", Pc_range)
    print("Pm range:", Pm_range)
    print("epsilon:", epsilon)
    print("alpha:", alpha)
    print("gamma:", gamma)
    print("_" * 30)

    # Load input parameters from file
    parameters = parser.parse(data_path)
   
    # Initialize the population
    population = encoding.initializePopulation(parameters)
    
    # Initialize the Q-table
    Q = initialize_Q_table(len(population))
    
    # Draw and save the initial Gantt chart
    initial_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
    initial_gantt_data = decoding.translate_decoded_to_gantt(
        decoding.decode(parameters, initial_best_individual[0], initial_best_individual[1])
    )
    print("Initial - Gantt data:", initial_gantt_data)
    print("Initial best (chromosome):", initial_best_individual[0])
    print("Initial best (machine allocation):", initial_best_individual[1])
    print("Parameters:", parameters)
    gantt.draw_chart(initial_gantt_data, os.path.join(output_folder, "initial_gantt.svg"))
    print(f"Initial Gantt chart saved in '{output_folder}'.")
    t0 = time.time()  # Start time

    gen = 1  # Generation count
    use_sarsa = True  # Start with SARSA

    # List to record convergence, parameter adaptation, and reward data at each generation
    steps = []
    print("Starting loop...")
    
    # Evaluate population and iterate
    while not termination.shouldTerminate(population, gen) and no_improvement_count < max_no_improvement_generations:
        print(f"Generation {gen}")
        best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        best_time = genetic.timeTaken(best_individual, parameters)
        avg_time = np.mean([genetic.timeTaken(ind, parameters) for ind in population])
        print(f"Best time in generation {gen}: {best_time}")
        print(f"Average time in generation {gen}: {avg_time}")

        # Check improvement
        if best_time == previous_best_time:
            no_improvement_count += 1
        else:
            no_improvement_count = 0
        previous_best_time = best_time

        # Select action using epsilon-greedy strategy
        state = gen % len(population)
        # Initialize Pc and Pm; these will be adjusted based on the RL action
        Pc = random.uniform(*Pc_range)
        Pm = random.uniform(*Pm_range)
        if random.random() < epsilon:
            action = random.choice([0, 1])  # Explore
        else:
            action = np.argmax(Q[state])  # Exploit

        # Adjust Pc and Pm based on the selected action
        if action == 0:
            Pc = random.uniform(*Pc_range)
        else:
            Pm = random.uniform(*Pm_range)

        # Apply genetic operators with the adjusted Pc and Pm
        population = genetic.selection(population, parameters)
        population = genetic.crossover(population, parameters, Pc)  # Use Pc
        population = genetic.mutation(population, parameters, Pm)   # Use Pm

        # Choose the next action for SARSA
        if random.random() < epsilon:
            next_action = random.choice([0, 1])  # Explore
        else:
            next_action = np.argmax(Q[(gen + 1) % len(population)])  # Exploit

        # Update Q values using SARSA or Q-learning
        new_best_individual = min(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))
        new_best_time = genetic.timeTaken(new_best_individual, parameters)
        reward = (best_time - new_best_time) / best_time

        if use_sarsa:
            Q = update_Q_sarsa(Q, state, action, reward, (gen + 1) % len(population), next_action, alpha, gamma)
        else:
            Q = update_Q_qlearning(Q, state, action, reward, (gen + 1) % len(population), alpha, gamma)

        # Record data for convergence, parameter adaptation, and reward
        steps.append({
            'generation': gen, 
            'best_time': best_time, 
            'average_time': avg_time,
            'Pc': Pc,
            'Pm': Pm,
            'reward': reward
        })

        # Switch from SARSA to Q-learning after enough iterations
        if gen > (len(population) * 10):  
            use_sarsa = False

        gen += 1

    sortedPop = sorted(population, key=lambda cpl: genetic.timeTaken(cpl, parameters))

    t1 = time.time()  # End time
    total_time = t1 - t0  # Total execution time
    print("Completed in {0:.2f}s".format(total_time))

    # Draw and save the final Gantt chart
    final_gantt_data = decoding.translate_decoded_to_gantt(
        decoding.decode(parameters, sortedPop[0][0], sortedPop[0][1])
    )
    gantt.draw_chart(final_gantt_data, os.path.join(output_folder, "final_gantt.svg"))
    print(f"Final Gantt chart saved in '{output_folder}'.")

    # Save results and total time in a CSV file (including reward, Pc, and Pm values)
    csv_file = os.path.join(output_folder, "results.csv")
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['generation', 'best_time', 'average_time', 'Pc', 'Pm', 'reward']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for step in steps:
            writer.writerow(step)
        writer.writerow({'generation': 'Total Time', 'best_time': total_time, 'average_time': '', 'Pc': '', 'Pm': '', 'reward': ''})
    print(f"Results saved in '{csv_file}'.")

    # Generate and save the plots
    plot_convergence(steps, output_folder)
    plot_parameter_adaptation(steps, output_folder)
    plot_reward(steps, output_folder)

def main():
    data_dir = 'test_data/Barnes/Text'
    main_output_dir = 'comparison_results'
    
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)

    for file_name in os.listdir(data_dir):
        if file_name.endswith('.fjs'):
            data_path = os.path.join(data_dir, file_name)
            base_name = os.path.splitext(file_name)[0]
            output_folder = os.path.join(main_output_dir, base_name)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            print(f"Running genetic algorithm on {file_name}...")
            run_genetic_algorithm(data_path, output_folder)
            print(f"Finished processing {file_name}.\n")

if __name__ == "__main__":
    main()
