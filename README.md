# SpotiStats

A Streamlit web application that provides detailed insights into your Spotify listening habits, including top tracks, artists, genres, and recent listening patterns.

## Features

- View your top tracks and artists for different time periods
- See your recently played tracks
- Visualize your listening patterns
- Beautiful and interactive interface

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Av1Sharma/SpotiStats.git
cd SpotiStats
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Create a `.env` file with your Spotify credentials:
```
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

4. Run the app:
```bash
streamlit run streamlit_app.py
```

## Deployment on Streamlit Cloud

1. Fork this repository
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your forked repository
6. Set the main file path to `streamlit_app.py`
7. Add your Spotify credentials in the Streamlit secrets management:
```toml
[spotify]
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
redirect_uri = "https://share.streamlit.io/your-username/your-app-name/callback"
```

## Spotify Developer Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add these Redirect URIs:
   - `http://localhost:8888/callback` (for local development)
   - `https://share.streamlit.io/your-username/your-app-name/callback` (for deployed app)

## License

MIT License
