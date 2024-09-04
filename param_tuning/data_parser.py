import re


def get_cgp_ls_sa_dict_from_pipelines(pipeline_names,
                                      linked_list_of_mean_fitness_and_digraph,
                                      ls_results,
                                      sa_results):
    cgp_results = []

    if len(pipeline_names) == len(ls_results) == len(sa_results):
        for name in pipeline_names:
            if name in linked_list_of_mean_fitness_and_digraph.keys():
                cgp_results.append(linked_list_of_mean_fitness_and_digraph[name]["best_individual_fitness"])
            elif name == "MAIPreform2_Spule0_0315_Upside_Thread_256":
                cgp_results.append(linked_list_of_mean_fitness_and_digraph["MAIPreform2_Spule0-0315_Upside Thread 256"]["best_individual_fitness"])
            elif name == "MAIPreform2_Spule0_0315_Upside_Thread":
                cgp_results.append(linked_list_of_mean_fitness_and_digraph["MAIPreform2_Spule0-0315_Upside Thread"]["best_individual_fitness"])
            elif name == "MAIPreform2_Spule0_0816_Upside":
                cgp_results.append(linked_list_of_mean_fitness_and_digraph["MAIPreform2_Spule2-0816_Upside"]["best_individual_fitness"])
            elif name == "MAIPreform2_Spule0_0315_Upside":
                cgp_results.append(linked_list_of_mean_fitness_and_digraph["MAIPreform2_Spule0-0315_Upside"]["best_individual_fitness"])
            elif name == "MVTec_AD_Leather":
                cgp_results.append(linked_list_of_mean_fitness_and_digraph["MVTec_D_Leather"]["best_individual_fitness"])
    else:
        raise ValueError("Arrays have different sizes.")

    return cgp_results


def get_line_pattern():
    # Regular expressions for each part of the structure
    iteration_pattern = r'-?\d+'
    performance_pattern = r'\d+\.\d+'
    criterion_pattern = r'\w+'
    parameters_pattern = r'(\d+, )*\d+, ?'  # match comma-separated integers with optional trailing space
    algorithm_pattern = r'(\w+:\d+\.\d+,?)+'
    configuration_pattern = r'\w+'
    pipeline_pattern = r'[\w_]+'
    datetime_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}'

    # Combine all patterns into one
    line_pattern = re.compile(
        rf'{iteration_pattern};'
        rf'{performance_pattern};'
        rf'{criterion_pattern};'
        rf'{parameters_pattern};'
        rf'{algorithm_pattern};'
        rf'{configuration_pattern};'
        rf'{pipeline_pattern};'
        rf'{datetime_pattern};'
    )

    return line_pattern


def get_header_pattern():
    return "Iteration; Performance; Criterion; Parameters; Algorithm; Configuration; Pipeline; Datetime;\n"


def extract_fitness_values(file_paths):
    sa_results = []
    ls_results = []

    for file_path in file_paths:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Filter out the relevant lines for SA and LS
            sa_best = None
            ls_best = None

            if lines[0] != get_header_pattern():
                print("!!! ERROR: File header compromised !!!")
                print("Aborting ...")
                return [], []

            for line in lines:
                parts = line.strip().split(';')
                if line != get_header_pattern():
                    if len(parts) >= 5:  # Ensure line has enough parts to be valid
                        iteration = int(parts[0].strip())
                        performance = float(parts[1].strip())
                        if parts[4] == "sa" or parts[4] == "ls":
                            algorithm = parts[4].strip().lower()
                        else:
                            algorithm = parts[5].strip().lower()

                        if algorithm == 'sa':
                            curr_sa_best = performance
                        elif algorithm == 'ls':
                            curr_ls_best = performance

                        # Assuming the last iteration (99) has the best performance
                        if iteration == 99:
                            if algorithm == 'sa':
                                sa_best = performance
                            elif algorithm == 'ls':
                                ls_best = performance

            # Append the best results to the lists
            if sa_best is not None:
                sa_results.append(sa_best)
                sa_best = None
            if ls_best is not None:
                ls_results.append(ls_best)
                ls_best = None

            if len(ls_results) != len(sa_results):
                print("WARNING: SA and LS Result Array mismatch!")
                if len(ls_results) < len(sa_results):
                    ls_results.append(0.0)
                else:
                    sa_results.append(0.0)

    return sa_results, ls_results
