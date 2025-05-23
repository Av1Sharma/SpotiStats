import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    st.title("Spotify Authentication Callback")
    
    try:
        # Get credentials from Streamlit secrets
        secrets = st.secrets["spotify"]
        
        # Set up the auth manager
        auth_manager = SpotifyOAuth(
            scope="user-top-read user-read-recently-played user-library-read",
            redirect_uri="https://spotistats.streamlit.app/spotify-callback",
            client_id=secrets["client_id"],
            client_secret=secrets["client_secret"],
            show_dialog=True,
            open_browser=False,
            cache_handler=None
        )
        
        # Get the code from URL parameters
        if 'code' in st.query_params:
            code = st.query_params['code']
            
            # Exchange the code for a token
            token_info = auth_manager.get_access_token(code)
            
            # Create Spotify client
            sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test the connection
            user = sp.current_user()
            
            # Set session state
            st.session_state.authenticated = True
            st.session_state.sp = sp
            st.session_state.token_info = token_info
            
            # Force redirect to main page and refresh
            st.markdown("""
            <script>
                window.location.href = 'https://spotistats.streamlit.app/';
            </script>
            """, unsafe_allow_html=True)
            
        else:
            st.error("No authorization code received")
            st.markdown("""
            <script>
                window.location.href = 'https://spotistats.streamlit.app/';
            </script>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        st.markdown("""
        <script>
            window.location.href = 'https://spotistats.streamlit.app/';
        </script>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 