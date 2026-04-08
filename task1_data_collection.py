import requests
import time
from datetime import datetime
import json
import os

# Used to fetch a list of IDs of the current top stories on HackerNews
TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
#  This is a parameterized URL used to retrieve the detailed information for a specific HackerNews item
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
# The `User-Agent` header is included in all API requests for Identification and API monitoring
headers = {'User-Agent': 'TrendPulse/1.0'}

# Step 1 — Get the list of top story IDs:

print("Fetching top story IDs from HackerNews:")
# Created an empty list to store the story IDs
top_story_ids = []
# Task 1 — Make the API Calls
# Using try and except block, If a request fails, it will print a message and move on instead of crashing the script
try:
      response = requests.get(TOP_STORIES_URL, headers=headers) # used to fetch top story IDs.
      response.raise_for_status() # used to get the status code
      top_story_ids = response.json() # the received story IDs are saved under top_story_ids
except requests.exceptions.HTTPError as http_err: # will print the status code of the error if received
      print(f"HTTP error occurred while fetching top story IDs: {http_err}")
except requests.exceptions.RequestException as req_err: # will help to catch error related to network problems, connection errors, timeouts, invalid URLs,etc
    print(f"Error fetching top story IDs: {req_err}")

# Fetching the first 500
num_stories = 500
story_ids_to_fetch = top_story_ids[:num_stories] # Slicing the list to get the first 500 stories
print(f"Fetched story IDs. Will attempt to process the top {num_stories}.")

# Step 2 — Get each story's details:
# Created an empty list to store the story details
stories = []
print("Fetching details for each story")
for i, story_id in enumerate(story_ids_to_fetch): # used enumerate to access both the index and story_id using for loop
  try:
    story_response = requests.get(ITEM_URL.format(story_id), headers=headers) # in the url story_id is placed in the place holder
    story_response.raise_for_status() # used to get the status code
    story_data = story_response.json() # the received json response is saved under story_data
    if story_data and story_data.get('title'): # story_data is checked to see if data is present or not, if data is present checks if the title key exists and has a truthy value
      stories.append(story_data) # if above both the conditions are returned true the story data will be added to stories list.
  except requests.exceptions.HTTPError as http_err:  # will print the status code of the error if received
        print(f"HTTP error occurred while fetching details for story ID {story_id}: {http_err}")
  except requests.exceptions.RequestException as req_err: # will help to catch errors other than status code
        print(f"Error fetching details for story ID {story_id}: {req_err}")
  if (i+1) % 50 == 0: # condition to see if 50 stories were fetched
      print(f"Processed {i + 1}/{len(story_ids_to_fetch)} stories")
print(f"Successfully fetched details for {len(stories)} stories.")

# Below categories & keywords are used to assign a category to each story by checking whether its title contains any of these keywords.
categories_keywords = {
    'technology': ['AI', 'software', 'tech', 'code', 'computer', 'data', 'cloud', 'API', 'GPU', 'LLM'],
    'worldnews': ['war', 'government', 'country', 'president', 'election', 'climate', 'attack', 'global'],
    'sports': ['NFL', 'NBA', 'FIFA', 'sport', 'game', 'team', 'player', 'league', 'championship'],
    'science': ['research', 'study', 'space', 'physics', 'biology', 'discovery', 'NASA', 'genome'],
    'entertainment': ['movie', 'film', 'music', 'Netflix', 'game', 'book', 'show', 'award', 'streaming']
}

def assign_category(title,categories_keyword): # This function lowercases the story title and checks for the presence of any keyword from `categories_keywords`.
  title_lower = title.lower() # since python is case-sensitive ensuring all the letters in title are in lower case so that it matches with the keywords in category.
  for category, keywords in categories_keywords.items(): #loop to access keys and values from categories_keywords
    for keyword in keywords: # loop to access each keyword in the list
      if keyword.lower() in title_lower: # converts the accessed keyword to lowercase and check if it is present in title_lower
        return category # if yes, it will return the category
  return 'uncategorized' # if not it will return uncategorized

# Categorize the fetched stories
categorized_stories = {category: [] for category in categories_keywords.keys()} # uses a dictionary comprehension to create an empty dictionary, for each category, it creates an empty list as its value.
categorized_stories['uncategorized'] = [] # explicitly adds another key to the this dictionary to store any stories that don't match keywords in any of the predefined categories.

for story in stories: # loop to iterate through the list of stories
    category = assign_category(story['title'], categories_keywords) # calls the function and the value returned is assigned to category
    categorized_stories[category].append(story) # This line adds category as key and story as value to categorized_stories dictionary

print("\n--- Categorized HackerNews Stories ---")
for category, story_list in categorized_stories.items(): # loop to iterate through categorized_stories dictionary to access both keys and values
  print(f"\nCategory: {category.upper()} ({len(story_list)}) stories")
  if story_list: # checks if the value returned is not none
    for story in story_list: # loop to iterate through story_list to access each story
      print(f" - {story['title']} (URL: {story.get('url','N/A')})") 
  else:
    print("  No stories in this category.")
  time.sleep(2) # Add a 2-second delay between categories

final_output = {
    'collected_at': datetime.now().isoformat(),
    'categories': {}
}

stories_per_category_limit = 25

# Task 2 — Extract the Fields
for category, stories_list in categorized_stories.items():
    processed_stories = [] # created empty list to save the processed story with the required fields
    for story in stories_list[:stories_per_category_limit]: # Limit to 25 stories per category
        processed_story = {
            'post_id': story.get('id'),
            'title': story.get('title'),
	    'category': category,
            'score': story.get('score'),
            'num_comments': story.get('descendants', 0),
            'author': story.get('by'),
            'collected_at': datetime.fromtimestamp(story.get('time')).isoformat() if story.get('time') else None
        }
        processed_stories.append(processed_story)
    final_output['categories'][category] = processed_stories

# Create data directory if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Save the data to a dated JSON file
datestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_filename = os.path.join(data_dir, f'trends_{datestamp}.json')

with open(output_filename, 'w') as f:
    json.dump(final_output, f, indent=4)

# Calculate total collected stories for the console message
total_collected_stories = sum(len(stories_list) for stories_list in final_output['categories'].values())

print(f"Collected {total_collected_stories} stories. Saved to {output_filename}")

