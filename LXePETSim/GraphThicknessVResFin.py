import argparse
import matplotlib.pyplot as plt
import os

def read_data(filename):
    x_vals = []
    y_vals = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 2:
                continue  # skip malformed lines
            try:
                x = float(parts[0])  # Add 19 to x
                y = float(parts[1])
                x_vals.append(x)
                y_vals.append(y)
            except ValueError:
                continue  # skip non-numeric values

    return x_vals, y_vals

def plot_two_files(file1, file2):
    x1, y1 = read_data(file1)
    x2, y2 = read_data(file2)

    label1 = "LXe"
    label2 = "LYSO"

    output_name = f"PercentHitsinEnergyWindow.png"

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(x1, y1, marker='o', linestyle='-', label=label1)
    plt.plot(x2, y2, marker='s', linestyle='--', label=label2)
    plt.xlabel("Thickness of Crystal (mm)")
    plt.ylabel("% of Hits Kept in by Energy Window")
    plt.title("Comparison of % of Hits Kept in by Energy Window: LXe v. LYSO")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_name)
    print(f"Plot saved to: {output_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot and compare two datasets with X shifted by +19.")
    parser.add_argument("file1", type=str, help="First input data file.")
    parser.add_argument("file2", type=str, help="Second input data file.")
    args = parser.parse_args()

    plot_two_files(args.file1, args.file2)
