import time
import googlemaps  # pip install googlemaps
import pandas as pd  # pip install pandas

###################################This section is added to prevent security issues for API key - not required for personal use ###########################################
from dotenv import load_dotenv
import os

# Explicitly load the .env file 
load_dotenv()
api_key = os.getenv("API_KEY")
print(f"api: {api_key}")
API_KEY = api_key
##########################################################################################################################################################################

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0


map_client = googlemaps.Client(API_KEY)

address = '700, Tainan City, West Central District, Puji Street, 53號咖哩鬥陣'
geocode = map_client.geocode(address=address)
(lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))

search_string = 'curry'
distance = miles_to_meters(0.621371)
business_list = []

response = map_client.places_nearby(
    location=(lat, lng),
    keyword=search_string,
    radius=distance
)

business_list.extend(response.get('results'))
next_page_token = response.get('next_page_token')

while next_page_token:
    time.sleep(2)
    response = map_client.places_nearby(
        location=(lat, lng),
        keyword=search_string,
        radius=distance,
        page_token=next_page_token
    )
    business_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

df = pd.DataFrame(business_list)

# Define threshold for user ratings
N = 300  # Replace with your desired threshold

# Add a new column based on the condition
df['is_popular'] = df['user_ratings_total'].apply(lambda x: x > N if pd.notnull(x) else False)

# Count the number of "True" values in the "is_popular" column
popular_count = df['is_popular'].sum()


print(f"Number of popular businesses: {popular_count}")
# Add Google Maps URL column
df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']

# Export to Excel
df.to_excel(f'{search_string}.xlsx', index=False)

# Filter the DataFrame to only include rows where "is_popular" is True
popular_df = df[df['is_popular']]

# Export the filtered DataFrame to Excel
popular_df.to_excel(f'{search_string}_popular.xlsx', index=False)

print(f"Exported {len(popular_df)} popular businesses to {search_string}_popular.xlsx")
