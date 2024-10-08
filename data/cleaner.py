import pandas as pd

# Load the datasets
spotify_df = pd.read_csv('spotify_most_streamed_songs.csv')
events_df = pd.read_csv('world_important_events.csv')
gdp_df = pd.read_csv('gdp_data.csv')

gdp_cleaned=gdp_df[['Year', 'Growth']]
gdp_cleaned['Growth']=gdp_cleaned['Growth'].apply( lambda x: (float(x.strip('%'))) if isinstance(x, str) else (x * 100))

# Clean and aggregate Spotify streams data
streams_cleaned = spotify_df[['streams', 'bpm', 'energy_%', 'speechiness_%']]
streams_cleaned = streams_cleaned.dropna()

# Normalize 'energy_%' and 'speechiness_%' to a 0-100 scale
streams_cleaned['energy_%'] = streams_cleaned['energy_%'].apply(lambda x: x * 100 if x <= 1 else x)
streams_cleaned['speechiness_%'] = streams_cleaned['speechiness_%'].apply(lambda x: x * 100 if x <= 1 else x)

# Clean Spotify dataset and remove NaN values
spotify_cleaned = spotify_df[['released_year', 'bpm', 'valence_%', 'energy_%', 'liveness_%']]
spotify_cleaned = spotify_cleaned.dropna()

# Normalize 'valence_%', 'energy_%', and 'liveness_%' to a 0-100 scale
spotify_cleaned['valence_%'] = spotify_cleaned['valence_%'].apply(lambda x: x * 100 if x <= 1 else x)
spotify_cleaned['energy_%'] = spotify_cleaned['energy_%'].apply(lambda x: x * 100 if x <= 1 else x)
spotify_cleaned['liveness_%'] = spotify_cleaned['liveness_%'].apply(lambda x: x * 100 if x <= 1 else x)


spotify_aggregated = spotify_cleaned.groupby('released_year').agg({
    'valence_%': 'mean',
    'bpm': 'mean',
    'liveness_%': 'mean',
    'energy_%': 'mean'
}).reset_index()

spotify_aggregated.columns = ['Year', 'Avg_Valence', 'Avg_BPM', 'Avg_Liveness', 'Avg_Energy']

events_cleaned = events_df.drop(columns=['Sl. No', 'Place Name', 'Affected Population', 'Month', 'Date', 'Important Person/Group Responsible'])

events_cleaned['Year'] = pd.to_numeric(events_cleaned['Year'], errors='coerce')
events_cleaned = events_cleaned.dropna(subset=['Year'])

events_cleaned = events_cleaned[~events_cleaned['Name of Incident'].str.contains('Unknown', case=False, na=False)]

events_aggregated = events_cleaned.groupby('Year').agg({
    'Name of Incident': lambda x: ', '.join(x)  # Concatenate event names with commas
}).reset_index()

events_aggregated.columns = ['Year', 'Events']

merged_df = pd.merge(spotify_aggregated, gdp_cleaned, on='Year', how='right')

print(merged_df.head())

merged_df.to_csv('cleaned_data.csv', index=False)
streams_cleaned.to_csv('cleaned_streams.csv', index=False)
