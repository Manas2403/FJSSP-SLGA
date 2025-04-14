# FJSSP-SLGA: Self-Learning Genetic Algorithm for Flexible Job Shop Scheduling

This repository presents a Self-Learning Genetic Algorithm (SLGA) for solving the Flexible Job Shop Scheduling Problem (FJSSP), a complex and NP-hard optimization problem. The solution integrates reinforcement learning with traditional genetic algorithms to adaptively improve scheduling performance.

---

## 📁 Repository Structure

```
FJSSP-SLGA/
├── data/          # Input files with job and machine configurations
├── results/       # Output files and metrics generated after execution
├── src/           # Source code implementing the SLGA
├── .gitignore     # Files and folders ignored by Git
├── README.md      # Project documentation
```

---

## 🧠 Project Overview

This project addresses the **Flexible Job Shop Scheduling Problem (FJSSP)**—a well-known NP-hard optimization problem—by applying a hybrid of **Genetic Algorithms (GA)** and **Reinforcement Learning (RL)** techniques, including:

- **SARSA**
- **Q-Learning**

---

## 🚀 Key Features

- 🔀 **Dynamic Machine Assignment**: Jobs can be flexibly assigned to different machines; the algorithm learns the optimal routing.
- 🧬 **Hybrid Optimization**: Combines Genetic Algorithms with RL to enhance both global search and local decision-making.
- 📊 **Algorithm Comparison**: Evaluate and compare SARSA, Q-Learning on identical problem instances.
- 📈 **Visual Insights**: Generates Gantt charts, Convergence plots, Reward plots and Parameter adaptation plots for intuitive understanding of scheduling and optimization behavior.

---

## 🛠️ Setup and Installation

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone https://github.com/Manas2403/FJSSP-SLGA.git
cd FJSSP-SLGA
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Input Data

Add your job and machine configuration files to the `data/` directory. Files should follow the expected format describing operations, processing times, and available machines.

### 5. Run the Algorithm

```bash
python src/main.py
```

### 6. Review Results

Output results including optimized schedules and performance metrics will be saved to the `results/` folder.
