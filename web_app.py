from flask import Flask, render_template
from app import SpotifyStatsGenerator
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    stats_generator = SpotifyStatsGenerator()
    
    timeframes = {
        "Last 4 Weeks": "short_term",
        "Last 6 Months": "medium_term",
        "All Time": "long_term"
    }
    
    all_data = {}
    for title, time_range in timeframes.items():
        tracks_df, artists_df = stats_generator.get_stats_for_timeframe(time_range)
        all_data[title] = {
            'tracks': tracks_df.to_dict('records'),
            'artists': artists_df.to_dict('records')
        }
    
    recent = stats_generator.sp.current_user_recently_played(limit=50)
    recent_tracks = [{
        'name': item['track']['name'],
        'artist': item['track']['artists'][0]['name'],
        'played_at': item['played_at']
    } for item in recent['items']]
    
    return render_template('index.html', 
                         all_data=all_data,
                         recent_tracks=recent_tracks)

if __name__ == '__main__':
    app.run(debug=True) 