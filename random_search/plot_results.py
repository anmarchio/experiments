import os
import matplotlib.pyplot as plt

from settings import WDIR


def list_txt_files(results_dir):
    """Return all .txt files in the results directory."""
    if not os.path.isdir(results_dir):
        raise FileNotFoundError(f"Directory not found: {results_dir}")

    files = [f for f in os.listdir(results_dir) if f.lower().endswith(".txt")]
    files.sort()
    return files


def select_files(files):
    """Let the user select one or more files by index."""
    if not files:
        raise FileNotFoundError("No .txt files found.")

    print("Available .txt files:\n")
    for i, fname in enumerate(files, start=1):
        print(f"{i}: {fname}")

    print("\nSelect one or more files by number, separated by commas.")
    print("Example: 1,3,5")

    while True:
        choice = input("\nYour selection: ").strip()

        try:
            indices = [int(x.strip()) for x in choice.split(",") if x.strip()]
            indices = sorted(set(indices))

            if not indices:
                print("Please select at least one file.")
                continue

            if all(1 <= idx <= len(files) for idx in indices):
                return [files[idx - 1] for idx in indices]

            print(f"Please only enter numbers between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")


def parse_result_file(file_path):
    """
    Parse the txt result file into:
    - meta_lines: lines before '--- Iterations ---'
    - dataset_name: value from 'Name : ...'
    - iterations: x values
    - mcc_values: y values
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    meta_lines = []
    iterations = []
    mcc_values = []
    dataset_name = None

    in_iterations = False

    for line in lines:
        stripped = line.strip()

        if stripped == "--- Iterations ---":
            in_iterations = True
            continue

        if not in_iterations:
            meta_lines.append(line)

            # Parse the Name field, e.g.:
            # Name        : MP2_0315_Hole_256
            if ":" in line:
                left, right = line.split(":", 1)
                if left.strip().lower() == "name":
                    dataset_name = right.strip()
        else:
            if not stripped:
                continue

            # Expected format: iteration;value;
            parts = [p for p in stripped.split(";") if p != ""]
            if len(parts) >= 2:
                try:
                    iteration = int(parts[0])
                    mcc = float(parts[1])
                    iterations.append(iteration)
                    mcc_values.append(mcc)
                except ValueError:
                    pass

    return meta_lines, dataset_name, iterations, mcc_values


def print_meta_info(filename, meta_lines):
    """Print all meta information for one file."""
    print(f"\n{'=' * 60}")
    print(f"META INFO: {filename}")
    print(f"{'=' * 60}\n")
    for line in meta_lines:
        print(line)


def plot_multiple_mcc(file_data):
    """
    Plot MCC over iteration for multiple files.
    file_data: list of tuples (filename, dataset_name, iterations, mcc_values)
    """
    plt.figure(figsize=(12, 7))

    for filename, dataset_name, iterations, mcc_values in file_data:
        if not iterations or not mcc_values:
            print(f"No iteration data found in {filename}. Skipping plot.")
            continue

        paired = sorted(zip(iterations, mcc_values), key=lambda x: x[0])
        x_vals = [p[0] for p in paired]
        y_vals = [p[1] for p in paired]

        # Use Name field from file, fallback to filename without extension
        label = dataset_name if dataset_name else os.path.splitext(filename)[0]

        plt.plot(x_vals, y_vals, label=label)

    plt.title("Random Search MCC per iteration")
    plt.xlabel("Iteration")
    plt.ylabel("MCC")
    plt.ylim(-0.5, 0.5)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    results_dir = os.path.join(WDIR, "random_search", "results")

    try:
        files = list_txt_files(results_dir)
        selected_files = select_files(files)

        file_data = []

        for selected_file in selected_files:
            file_path = os.path.join(results_dir, selected_file)
            meta_lines, dataset_name, iterations, mcc_values = parse_result_file(file_path)

            print_meta_info(selected_file, meta_lines)
            file_data.append((selected_file, dataset_name, iterations, mcc_values))

        plot_multiple_mcc(file_data)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()