import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
import webbrowser

# Load environment variables for local development
if os.path.exists('.env'):
    load_dotenv()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'sp' not in st.session_state:
    st.session_state.sp = None
if 'token_info' not in st.session_state:
    st.session_state.token_info = None

def authenticate_spotify():
    """Handle Spotify authentication"""
    if not st.session_state.authenticated:
        try:
            # Get credentials from Streamlit secrets
            secrets = st.secrets["spotify"]
            
            # Define the exact redirect URI
            redirect_uri = "https://spotistats.streamlit.app/spotify-callback"
            
            # Set up the auth manager without opening a local server
            auth_manager = SpotifyOAuth(
                scope="user-top-read user-read-recently-played user-library-read",
                redirect_uri=redirect_uri,
                client_id=secrets["client_id"],
                client_secret=secrets["client_secret"],
                show_dialog=True,
                open_browser=False,  # Don't try to open browser automatically
                cache_handler=None  # Disable caching to prevent issues
            )
            
            # Get the authorization URL
            auth_url = auth_manager.get_authorize_url()
            
            # Display debug information
            st.write("Debug Information:")
            st.write(f"Redirect URI: {redirect_uri}")
            st.write(f"Client ID: {secrets['client_id']}")
            
            # Display the authorization link
            st.markdown(f"""
            ### Step 1: Authorize with Spotify
            Click the link below to authorize with Spotify:
            
            [Sign in with Spotify]({auth_url})
            
            After authorizing, you will be redirected back to this page.
            """)
            
            return False
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.error("""
            Please check:
            1. Your Spotify Developer Dashboard settings
            2. The redirect URI is exactly: https://spotistats.streamlit.app/spotify-callback
            3. Your client ID and client secret are correct
            4. Try disabling any ad blockers or privacy extensions
            """)
            return False
    return True

def get_stats_for_timeframe(time_range, limit=20):
    """Get both tracks and artists for a specific time range"""
    sp = st.session_state.sp
    tracks = sp.current_user_top_tracks(
        limit=limit,
        offset=0,
        time_range=time_range
    )
    
    artists = sp.current_user_top_artists(
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
            'genres': ', '.join(item['genres'][:3]),
            'popularity': item['popularity'],
            'followers': item['followers']['total']
        }
        artist_data.append(artist_info)
        
    return pd.DataFrame(track_data), pd.DataFrame(artist_data)

def main():
    st.set_page_config(page_title="Spotify Stats", page_icon="🎵", layout="wide")
    
    st.title("🎵 Your Spotify Listening Stats")
    
    # Initialize session state if not already done
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'sp' not in st.session_state:
        st.session_state.sp = None
    if 'token_info' not in st.session_state:
        st.session_state.token_info = None
    
    # Check if we're returning from authentication
    if 'code' in st.query_params:
        st.rerun()
    
    if not st.session_state.authenticated:
        st.write("Please sign in with your Spotify account to view your listening statistics.")
        if st.button("Sign in with Spotify"):
            if authenticate_spotify():
                st.rerun()
    else:
        try:
            # Verify the connection is still valid
            user = st.session_state.sp.current_user()
            st.write(f"Welcome back, {user['display_name']}!")
            
            # Add a sign out button at the top
            if st.button("Sign Out"):
                st.session_state.authenticated = False
                st.session_state.sp = None
                st.session_state.token_info = None
                st.rerun()
            
            timeframes = {
                "Last 4 Weeks": "short_term",
                "Last 6 Months": "medium_term",
                "All Time": "long_term"
            }
            
            selected_timeframe = st.selectbox(
                "Select Time Period",
                list(timeframes.keys())
            )
            
            tracks_df, artists_df = get_stats_for_timeframe(timeframes[selected_timeframe])
            
            # Display stats in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top Tracks")
                st.dataframe(
                    tracks_df[['rank', 'name', 'artist', 'popularity']],
                    hide_index=True
                )
                
                # Plot track popularity
                fig, ax = plt.subplots(figsize=(10, 6))
                tracks_df.plot(kind='bar', x='name', y='popularity', ax=ax)
                plt.xticks(rotation=45, ha='right')
                plt.title('Track Popularity')
                st.pyplot(fig)
            
            with col2:
                st.subheader("Top Artists")
                st.dataframe(
                    artists_df[['rank', 'name', 'genres', 'popularity']],
                    hide_index=True
                )
                
                # Plot artist popularity
                fig, ax = plt.subplots(figsize=(10, 6))
                artists_df.plot(kind='bar', x='name', y='popularity', ax=ax)
                plt.xticks(rotation=45, ha='right')
                plt.title('Artist Popularity')
                st.pyplot(fig)
            
            st.subheader("Recently Played")
            recent = st.session_state.sp.current_user_recently_played(limit=50)
            recent_tracks = pd.DataFrame([{
                'name': item['track']['name'],
                'artist': item['track']['artists'][0]['name'],
                'played_at': datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            } for item in recent['items']])
            
            st.dataframe(
                recent_tracks[['name', 'artist', 'played_at']],
                hide_index=True
            )
            
        except Exception as e:
            st.error(f"Error loading your stats: {str(e)}")
            st.session_state.authenticated = False
            st.session_state.sp = None
            st.session_state.token_info = None
            st.rerun()

if __name__ == "__main__":
    main() 