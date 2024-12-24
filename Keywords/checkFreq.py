import pandas as pd
from rake_nltk import Rake

# Step 1: Load the Excel file
file_path = "google reviews with english translations.xlsx"  # Replace with your file path
column_name = "translation"    # Replace with your column name

# Read the Excel file
df = pd.read_excel(file_path)
reviews = df[column_name].dropna()  # Remove any empty rows

# Step 2: Initialize RAKE
rake = Rake()

# Step 3: Extract Keywords and Count Frequency
keywords_frequency = {}

for review in reviews:
    rake.extract_keywords_from_text(review)
    keywords = rake.get_ranked_phrases()  # Get keywords/phrases

    for keyword in keywords:
        keywords_frequency[keyword] = keywords_frequency.get(keyword, 0) + 1

# Step 4: Sort and Display Results
sorted_keywords = sorted(keywords_frequency.items(), key=lambda x: x[1], reverse=True)

print("Keyword Frequency:")
for keyword, frequency in sorted_keywords:
    print(f"{keyword}: {frequency}")
# Convert the sorted keyword frequency to a DataFrame
output_df = pd.DataFrame(sorted_keywords, columns=["Keyword", "Frequency"])

# Export the DataFrame to an Excel file
output_file = "keywords_frequency.xlsx"  # Specify your desired file name
output_df.to_excel(output_file, index=False)

print(f"Keyword frequency has been exported to {output_file}")
