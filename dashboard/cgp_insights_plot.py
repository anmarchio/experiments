import os
import json
import matplotlib.pyplot as plt
from graphviz import Source

from settings import WDIR, CGP_INSIGHTS_OUT, RESULTS_PATH

MIN_INCREASE = 0.01


def exists_or_create_dir(dir_path: str):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def create_plot(base_dir: str,
                folder_name: str,
                run: int,
                best_individual_fit: []):
    # Create line plot
    generations = list(range(len(best_individual_fit)))
    plt.figure(figsize=(10, 6))

    # Plot the fitness values
    plt.plot(best_individual_fit, generations, color="orange", linewidth=1.5, label="Fitness Progression")

    # Fill the area under the curve
    plt.fill_betweenx(generations, 0, best_individual_fit, color="orange", alpha=0.3)

    # Customize plot
    plt.xlabel("Fitness", fontsize=12)
    plt.ylabel("Generations", fontsize=12)
    plt.gca().invert_yaxis()  # Invert y-axis to read generations from top to bottom
    plt.title("Fitness Progression Across Generations\n" + folder_name + ", Run " + str(run), fontsize=14)
    plt.legend()
    plt.grid(alpha=0.4)
    plt.tight_layout()

    # Show plot
    # plt.show()
    exists_or_create_dir(os.path.join(CGP_INSIGHTS_OUT, folder_name))
    fig_file_name = os.path.join(base_dir, folder_name, str(run) + "_evolution.png")
    plt.savefig(fig_file_name)


def print_pipelines_by_fitness_increase(base_dir: str,
                                        out_dir: str,
                                        pipeline_dir: str,
                                        run: int,
                                        best_individual_fit: [],
                                        min_increase: float):
    # Step 2: Find high increase indices
    high_increase_indices = [
        i for i in range(1, len(best_individual_fit))
        if best_individual_fit[i] - best_individual_fit[i - 1] >= min_increase
    ]

    # Step 3: Map indices to pipeline files
    pipeline_files = []
    for idx in high_increase_indices:
        pipeline_name = f"pipeline_{idx}_of_{len(best_individual_fit) + 1}_in_Run_{run}"
        pipeline_path = os.path.join(base_dir, pipeline_dir, "Grid", str(run), "pipelines", pipeline_name + ".txt")
        if os.path.exists(pipeline_path):
            pipeline_files.append(pipeline_path)
        else:
            print(f"Warning: Pipeline file not found for index {idx} ({pipeline_name}.txt) in run {run}")

    # Step 4: Print and render DOT pipelines as graphs
    for pipeline_path in pipeline_files:
        print(f"Rendering pipeline graph from: {pipeline_path}")
        with open(pipeline_path, "r") as file:
            dot_content = file.read()
        # Render graph
        graph = Source(dot_content)
        # graph.view()  # Opens the graph in the default viewer (or saves as PDF if configured)

        graph_file_name = os.path.join(out_dir, pipeline_dir, os.path.split(pipeline_path)[-1])
        graph.save(graph_file_name)
        graph.render(filename=graph_file_name, format='jpg')


def plot_cgp_insights():
    base_dir = os.path.join(RESULTS_PATH, "cgp_insights")
    exists_or_create_dir(os.path.join(CGP_INSIGHTS_OUT))

    # Walk through each folder and extract fitness values
    for folder_name in sorted(os.listdir(base_dir)):
        exists_or_create_dir(os.path.join(CGP_INSIGHTS_OUT, folder_name))

        best_individual_fit = []
        folder_path = os.path.join(base_dir, folder_name)

        if os.path.isdir(folder_path):
            runs = len(os.listdir(os.path.join(folder_path, "Analyzer")))
            for run in range(runs):
                json_path = os.path.join(folder_path, "Analyzer", str(run), "BestIndividualFit.json")
                if os.path.exists(json_path):
                    with open(json_path, "r") as file:
                        data = json.load(file)
                        # Extract 'BestIndividualFit' and add to list
                        for i in range(len(data) - 1):
                            if "BestIndividualFitness" in data[i]:
                                best_individual_fit.append(data[i]["BestIndividualFitness"])
                            else:
                                print(f"Warning: 'BestIndividualFitness' not found in {json_path}")

                create_plot(CGP_INSIGHTS_OUT, folder_name, run, best_individual_fit)

                print_pipelines_by_fitness_increase(base_dir, CGP_INSIGHTS_OUT,
                                                    folder_name, run, best_individual_fit, MIN_INCREASE)
