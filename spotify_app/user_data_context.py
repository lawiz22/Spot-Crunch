import json
import base64
import requests

# Authentication Steps, paramaters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

#  Client Keys
CLIENT = json.load(open('keys.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']
BASE64 = base64.b64encode(bytes(CLIENT_ID + ':' + CLIENT_SECRET, 'ascii'))
BASE64 = BASE64.decode('ascii')

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-library-read user-read-currently-playing user-top-read user-library-modify user-follow-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# Parameters combine in one part
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)


# Context to use in authorizations/callback
def user_context(request):
    ctx = {
        'url_args': url_args,
        'auth_url': auth_url
    }
    return ctx

# -=-=-=-=-=-=-=-=-= Endpoints =-=-=-=-=-=-=-=-=-=


USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PROFILE_TOP_ARTISTS = "{}/{}".format(USER_PROFILE_ENDPOINT, 'top/artists/')
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played?limit=50')
USER_CURRENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'currently-playing')                                                  
USER_SAVE_TRACKS = "{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'tracks')
USER_SAVE_TRACKS_C = "{}/{}".format(USER_SAVE_TRACKS,
                                                  'contains')                                                  
NEW_RELEASES_ENDPOINT = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse', 'new-releases')


# https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
def get_users_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()    

# GET https://api.spotify.com/v1/me/player/currently-playing
def get_users_currently_played(auth_header):
    url = USER_CURRENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# GET https://api.spotify.com/v1/me/top/artists
def get_users_top_artist(auth_header):
    url = USER_PROFILE_TOP_ARTISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/browse/new-releases
def get_new_releases(auth_header):
    url = NEW_RELEASES_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/albums/{id}
def get_album(auth_header, album_id):
    url = "{}/{}/{}".format(SPOTIFY_API_URL, 'albums', album_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}
def get_spotify_playlist(auth_header, playlist_id):
    url = "{}/users/spotify/playlists/{}?market=US".format(SPOTIFY_API_URL, playlist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks
def get_playlist_tracks(auth_header, playlist_id):
    url = "{}/users/spotify/playlists/{}/tracks?market=US&limit=50".format(SPOTIFY_API_URL, playlist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/audio-features/{id}
def get_track_audio_features(auth_header, track_id):
    url = "{}/audio-features/{}".format(SPOTIFY_API_URL, track_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://api.spotify.com/v1/tracks/{id}
def get_track(auth_header, track_id):
    url = "{}/tracks/{}".format(SPOTIFY_API_URL, track_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()    

# https://api.spotify.com/v1/me/tracks/contains
def get_save_track(auth_header, track_id):
    url = "{}/me/tracks/contains?ids={}".format(SPOTIFY_API_URL, track_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://api.spotify.com/v1/me/albums/contains
def get_save_albums(auth_header, album_id):
    url = "{}/me/albums/contains?ids={}".format(SPOTIFY_API_URL, album_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://api.spotify.com/v1/me/albums/contains
def push_save_albums(auth_header, album_id):
    url = "{}/me/albums/?ids={}".format(SPOTIFY_API_URL, album_id)
    resp = requests.put(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/search
def search_result(auth_header, searching):
    url = "{}/search?q={}&type=artist".format(SPOTIFY_API_URL, searching)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/artists/{id}/albums
def artist_albums(auth_header, artist):
    url = "{}/artists/{}/albums?album_type=album".format(SPOTIFY_API_URL, artist)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://api.spotify.com/v1/artists/{id}
def get_artist(auth_header, artist):
    url = "{}/artists/{}/".format(SPOTIFY_API_URL, artist)
    resp = requests.get(url, headers=auth_header)
    return resp.json()   

# https://api.spotify.com/v1/me/albums/contains
def get_save_artists(auth_header, artist_id):
    url = "{}/me/following/contains?type=artist&ids={}".format(SPOTIFY_API_URL, artist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()
 