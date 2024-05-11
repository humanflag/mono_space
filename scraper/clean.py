import pandas as pd
from tqdm.auto import tqdm

# Load the CSV file into a DataFrame, ensuring all entries are treated as strings
print("Loading data...")
df = pd.read_csv('output.csv', header=None, names=['user', 'post'], dtype=str, keep_default_na=False)
print("Data loaded.")

# Function to clean the 'post' column
def clean_post(post):
    # Find the index of the last occurrence of ' said:' and clean
    index = post.rfind(' said:')
    return post[index + len(' said:'):] if ' said:' in post else post

# Apply the cleaning function to the 'post' column with vectorized operations
print("Cleaning data...")
df['post'] = df['post'].apply(clean_post)
print("Data cleaned.")

# Remove rows with duplicate posts after cleaning
print("Removing duplicates...")
df = df.drop_duplicates(subset='post')
print("Duplicates removed.")

# Save the cleaned DataFrame back to a CSV file
# Ensure that quotes are preserved and properly escaped
df.to_csv('cleaned_output.csv', index=False, header=False, quoting=1)
print("Processing complete. The cleaned data is saved in 'cleaned_output.csv'.")
