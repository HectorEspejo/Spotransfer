import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost'  # The script will ask for the redirection URI

# Scope to access liked songs and manage playlists
scope = 'user-library-read playlist-modify-private playlist-modify-public'

# Authenticate and get the Spotify token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_liked_tracks(sp):
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [track['track']['id'] for track in tracks]

def add_tracks_to_playlist(sp, track_ids, playlist_id):
    sp.playlist_add_items(playlist_id, track_ids)

def main():
    # Get all liked tracks
    liked_tracks = get_liked_tracks(sp)

    # Create a new playlist or use an existing one
    user_id = sp.current_user()['id']
    playlist_name = 'Liked Songs Playlist'
    playlist_description = 'A playlist containing all my liked songs'
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description)

    # Add liked tracks to the playlist
    playlist_id = playlist['id']
    # Spotify API limits to 100 tracks per request, so we need to add in chunks
    for i in range(0, len(liked_tracks), 100):
        add_tracks_to_playlist(sp, liked_tracks[i:i + 100], playlist_id)

    print(f'Added {len(liked_tracks)} tracks to the playlist "{playlist_name}".')

if __name__ == '__main__':
    main()
