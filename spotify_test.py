import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Enter your Client ID & Secret
client_id = "6fb00a41d7e2493585f9cd764f91f9b3"
client_secret = "1286bc1ae6df486c94d55ae661580b9f"

# Authenticate API
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

# Get a list of top songs
results = sp.search(q="top hits", limit=10)

# Print the song list
for idx, track in enumerate(results["tracks"]["items"]):
    print(f"{idx + 1}: {track['name']} - {track['artists'][0]['name']}")
