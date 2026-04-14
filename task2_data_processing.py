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

df.drop_duplicates(subset=['post_id'], inplace=True)
print(f"Removed duplicated rows based on 'post_id' ")

df.dropna(subset=['post_id', 'title', 'score'], inplace=True)
print(f"Dropped rows where post_id, title, or score are missing")

# Convert 'score' to integer, coercing errors to NaN first, then dropping them
df['score'] = pd.to_numeric(df['score'], errors='coerce')
df.dropna(subset=['score'], inplace=True)
df['score'] = df['score'].astype(int)

df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce')
df.dropna(subset=['num_comments'], inplace=True)
df['num_comments'] = df['num_comments'].astype(int)

print("Converted 'score' and 'num_comments' to integer type.")
print(df[['score', 'num_comments']].dtypes)

df = df[df['score'] >= 5]
print("Removed stories where score is less than 5")

df['title'] = df['title'].str.strip()
print("Stripped extra spaces from the 'title' column.")

# Display basic info and head of the cleaned DataFrame
print("\nDataFrame Info after cleaning:")
df.info()
print("\nFirst 5 rows of the cleaned DataFrame:")
display(df.head())

data_dir = 'C:/Users/valin/Desktop/data' # Define the output directory

# Generate a dated filename for the CSV
datestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv_filename = os.path.join(data_dir, f'trends_clean.csv')

try:
    df.to_csv(output_csv_filename, index=False)
    print(f"Cleaned data successfully saved to {output_csv_filename}")
except Exception as e:
    print(f"Error saving cleaned data to CSV: {e}")

print("\nFirst 5 rows of cleaned DataFrame:")
print(df.head())
