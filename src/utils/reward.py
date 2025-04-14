
import matplotlib.pyplot as plt  # Import for plotting
import os

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