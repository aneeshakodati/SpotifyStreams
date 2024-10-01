import pandas as pd

spotify_df = pd.read_csv('spotify_most_streamed_songs.csv')
events_df = pd.read_csv('world_important_events.csv')

spotify_cleaned = spotify_df[['released_year', 'bpm', 'valence_%', 'energy_%', 'liveness_%']]

spotify_cleaned = spotify_cleaned.dropna()

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

events_aggregated = events_cleaned.groupby('Year').agg({
    'Name of Incident': lambda x: ', '.join(x)  
}).reset_index()

events_aggregated.columns = ['Year', 'Events']

merged_df = pd.merge(spotify_aggregated, events_aggregated, on='Year', how='left')

print(merged_df.head())

merged_df.to_csv('cleaned_data.csv', index=False)

