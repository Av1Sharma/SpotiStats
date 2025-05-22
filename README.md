# Spotify Stats Generator README

## Overview
**Spotify Stats Generator** is a Python script that provides detailed insights into your Spotify listening habits, including your top tracks, artists, genres, and recent listening patterns. It uses the Spotify Web API via the `spotipy` library to gather data and generates comprehensive statistics and visualizations.

---

## Features
- **Top Tracks & Artists**:
  - Displays your most played tracks and artists for different time ranges: the last 4 weeks, the last 6 months, and all time.
- **Genre Analysis**:
  - Identifies the most common genres in your top artists' profiles.
- **Listening Patterns**:
  - Analyzes your recent listening habits and visualizes them as a bar chart of hourly activity.
- **Consistent Favorites**:
  - Highlights tracks and artists that appear consistently across multiple timeframes.

---

## Prerequisites

### Required Libraries
Ensure you have the following Python libraries installed:
- `spotipy`
- `pandas`
- `matplotlib`

Install them using:
```bash
pip install spotipy pandas matplotlib
```
Spotify Developer Credentials
You will need a Spotify Developer Account and a registered app. Follow these steps to obtain your credentials:

Create a Spotify Developer Account:

Visit the Spotify Developer Dashboard.
Log in using your Spotify account or create a new one.
Create an Application:

Once logged in, go to the "Dashboard" and click on the Create an App button.
Fill out the required details (name, description, etc.) for your app.
Retrieve Client Credentials:

After creating the app, you’ll be able to view the Client ID and Client Secret.
Keep these credentials secure as they are required for authentication.
Set Redirect URI:

In the app settings on the Spotify Developer Dashboard, add a redirect URI: http://localhost:8888/callback.
This URI will be used during the OAuth authentication process to redirect you back to the application.

Clone or download this repository.
Open the script and replace the client_id and client_secret in the SpotifyStatsGenerator class with your Spotify app credentials.
Run the script using:
```bash
python app.py
```
