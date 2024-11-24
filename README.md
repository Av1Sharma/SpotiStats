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
