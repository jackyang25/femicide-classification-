import pandas as pd

def reduce_csv_file(input_filename, output_filename):
    df = pd.read_csv(input_filename, low_memory=False)


    subset_length = int(len(df) * 0.05)

    subset_df = df.head(subset_length)


    print(f"Saving reduced file as: {output_filename}")
    subset_df.to_csv(output_filename, index=False)

    print("Process completed.")

# Example usage
# reduce_csv_file("CleanTweets_NoLinks.csv", "development.csv")

chunk_size = 50000  
chunks = pd.read_csv("development.csv", chunksize=chunk_size, low_memory=False)
i = 0
for chunk in chunks:
    try:
        i += 1
        print(f"Processed {i * chunk_size} rows successfully.")
    except Exception as e:
        print(f"Error encountered in chunk {i}.")
        print(e)
        break
