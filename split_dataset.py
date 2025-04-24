import re
import pickle
from tqdm import tqdm

def read_custom_csv(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        current_record = []
        for line in file:
            if current_record and re.match(r'^\d+,\s*https?://', line):
                yield ''.join(current_record)
                current_record = []
            current_record.append(line)
        if current_record:
            yield ''.join(current_record)

def clean_tweet(tweet):
    # Remove leading and trailing quotes
    return tweet.strip('"')

def process_and_split_data(file_name, output_prefix, num_files):
    all_records = list(read_custom_csv(file_name))
    chunk_size = len(all_records) // num_files + (len(all_records) % num_files > 0)

    with tqdm(total=len(all_records), desc="Processing Records") as pbar:
        for i in range(num_files):
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            chunk = all_records[start_index:end_index]

            # Clean and extract the last column (tweet)
            tweets = [clean_tweet(record.split(',')[-1].strip()) for record in chunk]
            with open(f'{output_prefix}_{i+1}.pkl', 'wb') as f:
                pickle.dump(tweets, f)

            pbar.update(len(chunk))

# Parameters
input_csv = 'CleanTweets_NoLinks.csv'  # Replace with your CSV file name
output_prefix = 'output_tweet'          # Prefix for the output files
num_split_files = 10                    # Number of files to split into

# Process and split the data
process_and_split_data(input_csv, output_prefix, num_split_files)
