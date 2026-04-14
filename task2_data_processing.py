import json
import os
import pandas as pd
from datetime import datetime

data_dir = 'data' # Define the path to the data directory
json_filename = 'C:/Users/valin/Desktop/data/trends_20260408_235550.json'
json_filepath = json_filename

# check if filepath exists
if not os.path.exists(json_filepath):
  print("Error: File not found")
else:
  # load the json file
  with open(json_filepath, 'r') as f:
    raw_data = json.load(f)
# Flatten the nested structure into a list of stories
all_stories = []
for category, stories_list in raw_data['categories'].items():
    for story in stories_list:
        all_stories.append(story)

df = pd.DataFrame(all_stories)

print(f"Successfully loaded {len(all_stories)} stories into a DataFrame.")

#creating a pandas DataFrame for each story list
category_dataframes = {}

print("Creating DataFrames for each category...")
for category_name, stories_list in raw_data['categories'].items():
    if stories_list:
        category_df = pd.DataFrame(stories_list)
        category_dataframes[category_name] = category_df
        print(f"\n--- First 5 rows of '{category_name.upper()}' Category DataFrame ---")
        print(category_df.head())
    else:
        print(f"\nNo stories found for the '{category_name.upper()}' category.")
print("DataFrame Info after JSON loading:")
df.info()

print("\nMissing values count:")
df.isnull().sum()

print("\nSummary statistics of the Dataframe provided")
df.describe()

print("Since no data is missing and data looks clean not performing further steps and saving data to CSV file")

data_dir = 'C:/Users/valin/Desktop/data' # Define the output directory

# Generate a dated filename for the CSV
datestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv_filename = os.path.join(data_dir, f'hackernews_cleaned_stories_{datestamp}.csv')

try:
    df.to_csv(output_csv_filename, index=False)
    print(f"Cleaned data successfully saved to {output_csv_filename}")
except Exception as e:
    print(f"Error saving cleaned data to CSV: {e}")

print("\nFirst 5 rows of cleaned DataFrame:")
print(df.head())