import pandas as pd
import matplotlib.pyplot as plt
import os

# Task 1) Load trends_analysed.csv to dataframe
csv_filepath = 'data/trends_analysed.csv'
if not os.path.exists(csv_filepath):
    print(f"Error: File not found at {csv_filepath}")
else:
    df = pd.read_csv(csv_filepath)
    print("DataFrame loaded successfully from trends_analysed.csv")

# Create folder named outputs if not exist
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")
else:
    print(f"Directory already exists: {output_dir}")

# Task 2: Horizontal chart to show top 10 stories by score
top_10_stories = df.sort_values(by='score', ascending=False).head(10)

# Shorten title name if > 50 char
top_10_stories['short_title'] = top_10_stories['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

plt.figure(figsize=(12, 8))
plt.barh(top_10_stories['short_title'], top_10_stories['score'], color='skyblue')
plt.xlabel('Score')
plt.ylabel('Story Title')
plt.title('Top 10 Stories by Score')
plt.gca().invert_yaxis() # To display the highest score at the top
plt.tight_layout()
output_chart1_path = os.path.join(output_dir, 'chart1_top_stories.png')
plt.savefig(output_chart1_path)
plt.show()
print(f"Chart saved to {output_chart1_path}")

# Task 3: Bar chart to show how many stories came from each category
stories_per_category = df['category'].value_counts()

plt.figure(figsize=(10, 6))
stories_per_category.plot(kind='bar', color=plt.cm.Paired.colors)
plt.title('Number of Stories per Category')
plt.xlabel('Category')
plt.ylabel('Number of Stories')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
output_chart2_path = os.path.join(output_dir, 'chart2_categories.png')
plt.savefig(output_chart2_path)
plt.show()
print(f"Chart saved to {output_chart2_path}")

# Task 4: Scatter plot for score on x-axis and num_comments on y-axis
plt.figure(figsize=(10, 7))
scatter = plt.scatter(df['score'], df['num_comments'], c=df['is_popular'], cmap='coolwarm', alpha=0.7)
plt.title('Score vs. Number of Comments (Colored by Popularity)')
plt.xlabel('Score')
plt.ylabel('Number of Comments')

# Add legend
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Popular', 
               markerfacecolor=plt.cm.coolwarm(1.0), markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Not Popular', 
               markerfacecolor=plt.cm.coolwarm(0.0), markersize=10)
]
plt.legend(handles=legend_elements, title='Popularity')

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
output_chart3_path = os.path.join(output_dir, 'chart3_scatter.png')
plt.savefig(output_chart3_path)
plt.show()
print(f"Chart saved to {output_chart3_path}")

# Task 5: Combine all 3 charts in one figure (dashboard)

if 'top_10_stories' not in locals():
    top_10_stories = df.sort_values(by='score', ascending=False).head(10)
    top_10_stories['short_title'] = top_10_stories['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

if 'stories_per_category' not in locals():
    stories_per_category = df['category'].value_counts()

fig, axes = plt.subplots(2, 2, figsize=(20, 15))
fig.suptitle('TrendPulse Dashboard', fontsize=20, y=1.02)

# Chart 1: Top 10 Stories by Score
axes[0, 0].barh(top_10_stories['short_title'], top_10_stories['score'], color='skyblue')
axes[0, 0].set_xlabel('Score')
axes[0, 0].set_ylabel('Story Title')
axes[0, 0].set_title('Top 10 Stories by Score')
axes[0, 0].invert_yaxis()

# Chart 2: Number of Stories per Category
axes[0, 1].bar(stories_per_category.index, stories_per_category.values, color=plt.cm.Paired.colors)
axes[0, 1].set_title('Number of Stories per Category')
axes[0, 1].set_xlabel('Category')
axes[0, 1].set_ylabel('Number of Stories')
axes[0, 1].tick_params(axis='x', rotation=45)

# Chart 3: Score vs. Number of Comments (Colored by Popularity)
scatter = axes[1, 0].scatter(df['score'], df['num_comments'], c=df['is_popular'], cmap='coolwarm', alpha=0.7)
axes[1, 0].set_title('Score vs. Number of Comments (Colored by Popularity)')
axes[1, 0].set_xlabel('Score')
axes[1, 0].set_ylabel('Number of Comments')
axes[1, 0].grid(True, linestyle='--', alpha=0.6)

# Add legend to scatter plot
legend_elements_dashboard = [
    plt.Line2D([0], [0], marker='o', color='w', label='Popular', 
               markerfacecolor=plt.cm.coolwarm(1.0), markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Not Popular', 
               markerfacecolor=plt.cm.coolwarm(0.0), markersize=10)
]
axes[1, 0].legend(handles=legend_elements_dashboard, title='Popularity')

# Hide the fourth subplot as we only have 3 charts for a 2x2 layout
fig.delaxes(axes[1, 1])

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent overlap
output_dashboard_path = os.path.join(output_dir, 'dashboard.png')
plt.savefig(output_dashboard_path)
plt.show()
print(f"Dashboard saved to {output_dashboard_path}")