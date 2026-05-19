import matplotlib.pyplot as plt

def plot_histogram(filename):
    cardinalities = []
    
    # Read data from file
    with open(filename, 'r') as file:
        for line in file:
            if 'Cardinality:' in line:
                # Extract the cardinality value
                parts = line.split('|')
                for part in parts:
                    if 'Cardinality:' in part:
                        card_val = float(part.split(':')[1].strip())
                        cardinalities.append(card_val)
    
    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.hist(cardinalities, bins=15, edgecolor='black', alpha=0.7)
    plt.title('Histogram of Cardinalities')
    plt.xlabel('Cardinality')
    plt.ylabel('Frequency (Number of Seeds/Iterations)')
    plt.grid(axis='y', alpha=0.75)
    
    # Save and show
    plt.savefig('cardinalities_histogram.png')
    plt.show()

if __name__ == "__main__":
    import os
    # Get the directory of the current script to find the txt file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'cardinalis.txt')
    plot_histogram(file_path)
