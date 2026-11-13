
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import secret


def spotify_client():
    scope = "user-read-currently-playing"

    auth_manager = SpotifyOAuth(
        client_id=secret.SPOTIFY_CLIENT_ID,
        client_secret=secret.SPOTIFY_CLIENT_SECRET,
        redirect_uri=secret.SPOTIFY_REDIRECT_URI,
        scope=scope,
        cache_path=".spotify_cache"
    )

    return spotipy.Spotify(auth_manager=auth_manager)


def currently_playing():
    sp = spotify_client()

    track = sp.current_user_playing_track()

    if track is None or track.get("item") is None:
        return None

    song = track["item"]

    # Get album artwork
    images = song["album"].get("images", [])
    image_url = images[0]["url"] if images else None

    return {
        "name": song["name"],
        "artist": ", ".join(
            artist["name"] for artist in song["artists"]
        ),
        "album": song["album"]["name"],
        "image_url": image_url,
        "is_playing": track["is_playing"]
    }
