import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

class SpotifyStatsGenerator:
    def __init__(self):
        self.scope = "user-top-read user-read-recently-played user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=self.scope,
            redirect_uri="http://localhost:8888/callback",
            client_id="f5951833e8844b27b03790473e15bdf7",
            client_secret="eded67bab74b46fe98fabd17b028a7fe",
            show_dialog=True
        ))

    def get_stats_for_timeframe(self, time_range, limit=20):
        """Get both tracks and artists for a specific time range"""
        tracks = self.sp.current_user_top_tracks(
            limit=limit,
            offset=0,
            time_range=time_range
        )
        
        artists = self.sp.current_user_top_artists(
            limit=limit,
            offset=0,
            time_range=time_range
        )
        
        track_data = []
        for idx, item in enumerate(tracks['items']):
            track_info = {
                'rank': idx + 1,
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'popularity': item['popularity'],
                'album': item['album']['name']
            }
            track_data.append(track_info)
        
        artist_data = []
        for idx, item in enumerate(artists['items']):
            artist_info = {
                'rank': idx + 1,
                'name': item['name'],
                'genres': ', '.join(item['genres'][:3]),  # Limit to top 3 genres for clarity
                'popularity': item['popularity'],
                'followers': item['followers']['total']
            }
            artist_data.append(artist_info)
            
        return pd.DataFrame(track_data), pd.DataFrame(artist_data)

    def print_timeframe_stats(self, title, tracks_df, artists_df):
        """Print formatted stats for a given timeframe"""
        print(f"\n{'='*20} {title} {'='*20}")
        
        print("\nTop Tracks:")
        print(tracks_df[['rank', 'name', 'artist']].to_string(index=False))
        
        print("\nTop Artists:")
        print(artists_df[['rank', 'name', 'genres']].to_string(index=False))
        
        print(f"\nStats for {title}:")
        print(f"Most Popular Track: {tracks_df.loc[tracks_df['popularity'].idxmax(), 'name']} "
              f"by {tracks_df.loc[tracks_df['popularity'].idxmax(), 'artist']}")
        print(f"Most Popular Artist: {artists_df.loc[artists_df['popularity'].idxmax(), 'name']}")
        
        genres = [g.strip() for genres in artists_df['genres'].str.split(',') for g in genres if g.strip()]
        top_genres = pd.Series(genres).value_counts().head(3)
        print("\nTop Genres:")
        for genre, count in top_genres.items():
            print(f"- {genre}: {count} artists")
        print("\n")

    def generate_comprehensive_report(self):
        """Generate reports for all timeframes"""
        print("\n🎵 SPOTIFY LISTENING REPORT 🎵")
        print("Generating comprehensive statistics across different time periods...")
        
        timeframes = {
            "Last 4 Weeks": "short_term",
            "Last 6 Months": "medium_term",
            "All Time": "long_term"
        }
        
        all_tracks = {}
        all_artists = {}
        
        for title, time_range in timeframes.items():
            tracks_df, artists_df = self.get_stats_for_timeframe(time_range)
            all_tracks[title] = tracks_df
            all_artists[title] = artists_df
            self.print_timeframe_stats(title, tracks_df, artists_df)
        
        print("\n🔍 INTERESTING INSIGHTS 🔍")
        
        consistent_artists = set(all_artists["Last 4 Weeks"]['name']) & \
                           set(all_artists["Last 6 Months"]['name']) & \
                           set(all_artists["All Time"]['name'])
        
        if consistent_artists:
            print("\nYour Most Consistent Favorites (Artists in all timeframes):")
            for artist in consistent_artists:
                print(f"- {artist}")
        
        consistent_tracks = set(all_tracks["Last 4 Weeks"]['name']) & \
                          set(all_tracks["Last 6 Months"]['name'])
        
        if consistent_tracks:
            print("\nTracks You've Loved for 6+ Months:")
            for track in consistent_tracks:
                print(f"- {track}")
        
        recent = self.sp.current_user_recently_played(limit=50)
        recent_tracks = pd.DataFrame([{
            'name': item['track']['name'],
            'artist': item['track']['artists'][0]['name'],
            'played_at': datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        } for item in recent['items']])
        
        if not recent_tracks.empty:
            recent_tracks['hour'] = recent_tracks['played_at'].dt.hour
            hourly_distribution = recent_tracks['hour'].value_counts().sort_index()
            
            plt.figure(figsize=(12, 6))
            hourly_distribution.plot(kind='bar')
            plt.title('Your Recent Listening Pattern by Hour of Day')
            plt.xlabel('Hour')
            plt.ylabel('Number of Tracks Played')
            plt.tight_layout()
            plt.savefig('listening_patterns.png')
            
            print("\n📊 Listening Pattern Analysis:")
            print(f"Most Active Listening Hour: {hourly_distribution.idxmax()}:00")
            print("A visualization of your listening patterns has been saved as 'listening_patterns.png'")

def main():
    try:
        print("Initializing Spotify Stats Generator...")
        stats_generator = SpotifyStatsGenerator()
        stats_generator.generate_comprehensive_report()
        print("\nReport generation complete! ✨")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please make sure your Spotify credentials are correct and you have authorized the application.")

if __name__ == "__main__":
    main()