import pandas as pd
import os
from datetime import datetime
import numpy as np

data_dir = 'data' # Define the path to the data directory
csv_filepath = 'C:/Users/valin/Desktop/data/trends_clean.csv' # filepathh
csv_file = csv_filepath

# check if filepath exists
if not os.path.exists(csv_file):
  print("Error: File not found")
else:
  # load the csv file
  with open(csv_file, 'r') as f:
    df = pd.read_csv(f, encoding='utf-8')

# Display basic info and head of the DataFrame
print("\nDataFrame Info after CSV loading:")
df.info()
print("\nFirst 5 rows of the loaded DataFrame:")
print(df.head())
print("\nShape of the DataFrame(rows) and columns")
print(df.shape)

# Calculate and print the average score
average_score = df['score'].mean()
print(f"\nAverage Score across all stories: {average_score:.2f}")

# Calculate and print the average number of comments
average_num_comments = df['num_comments'].mean()
print(f"Average Number of Comments across all stories: {average_num_comments:.2f}")

# Score statistics using numpy
mean_score = np.mean(df['score'])
median_score = np.median(df['score'])
std_score = np.std(df['score'])

print(f"\nScore Statistics:")
print(f"  Mean Score: {mean_score:.2f}")
print(f"  Median Score: {median_score:.2f}")
print(f"  Standard Deviation of Score: {std_score:.2f}")

# Highest and Lowest Score
highest_score = df['score'].max()
lowest_score = df['score'].min()

print(f"\nHighest Score: {highest_score}")
print(f"Lowest Score: {lowest_score}")

# Category with highest score
category_highest_score = df.loc[df['score'].idxmax(), 'category']
print(f"Category with the highest score story: {category_highest_score}")

# Story with most comments
story_most_comments = df.loc[df['num_comments'].idxmax()]
print(f"\nStory with the most comments:")
print(f"  Title: {story_most_comments['title']}")
print(f"  Number of Comments: {story_most_comments['num_comments']}")

# Calculate 'engagement' column
df['engagement'] = df['num_comments'] / (df['score'] + 1)
print("Added 'engagement' column.")

# Calculate 'is_popular' column
if 'average_score' not in locals():
    average_score = df['score'].mean()
df['is_popular'] = df['score'] > average_score
print(f"Added 'is_popular' column based on average score ({average_score:.2f}).")

# Display the DataFrame with the new columns
print("\nDataFrame with new 'engagement' and 'is_popular' columns:")
print(df.head())

data_dir = 'C:/Users/valin/Desktop/data' # Define the output directory

if not os.path.exists(data_dir): # Ensure the data directory exists
    os.makedirs(data_dir)

datestamp = datetime.now().strftime('%Y%m%d_%H%M%S') # Generate a dated filename for the CSV
output_csv_filename = os.path.join(data_dir, f'trends_analysed.csv')

df.to_csv(output_csv_filename, index=False) # Save the DataFrame to a CSV file

print(f"Cleaned data successfully saved to {output_csv_filename}")