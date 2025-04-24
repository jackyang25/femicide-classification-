import pickle

def print_pkl_contents(file_prefix, num_files):
    for i in range(1, num_files + 1):
        file_name = f'{file_prefix}_{i}.pkl'
        with open(file_name, 'rb') as file:
            # Load the contents of the pickle file
            data = pickle.load(file)

            # Print the contents
            print(f"Contents of {file_name}:")
            for item in data:
                print(item)
            print("\n---\n")

# Parameters
file_prefix = 'output_tweet'  # Prefix for the pickle files
num_files = 10               # Number of files to print

# Print the contents of each file
print_pkl_contents(file_prefix, num_files)
