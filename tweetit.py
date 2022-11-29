import json, tweepy, spotipy, time
from keys import *
from spotipy.oauth2 import SpotifyOAuth

#establish auth w/ access tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))

def auth(client_id, client_secret, redirect_uri, scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=scope))
    
def tweet_song(client_id, client_secret, redirect_uri, scope):
    #get currently platying track and parsing title/artist/album, formatting into tweet and publishing
    results = sp.current_user_playing_track()
    artist_name = results['item']['artists'][0]['name']
    song_name = results['item']['name']
    song_link = results['item']['external_urls']['spotify']
    album_name = results['item']['album']['name']
    hashtag = f'#{artist_name.replace(" ", "")}'
    tweet_string = f"I am now listening to 🔊\n🎶{song_name} - {artist_name}👨‍🎤\n💿Album - {album_name}💿\n{song_link}\n{hashtag}"
    print('now tweeting...')
    api.update_status(tweet_string)

#always re-establish auth to make sure never logged out or invalid bearer tokens
while True:
    try:
        auth(client_id, client_secret, redirect_uri, scope)
        current_track = sp.current_user_playing_track()
        current_track_id = current_track['item']['id']
        time.sleep(5)

        if current_track_id is not None:
            tweet_song(client_id, client_secret, redirect_uri, scope)
            break

        else:
            continue
            time.sleep(5) 

    except spotipy.oauth2.SpotifyOauthError as error:
        auth(client_id, client_secret, redirect_uri, scope)
        time.sleep(5)
        print(f'spotify error {error}')

    except BaseException as error:
        print(error)
        time.sleep(5)

while True:
    #address all scenarios that could be encountered (same song played/new song played/error occurs)
    try:
        auth(client_id, client_secret, redirect_uri, scope)
        new_track = sp.current_user_playing_track()
        new_track_id = new_track['item']['id']
        time.sleep(5)

        if current_track_id is not None and new_track_id != current_track_id:
            tweet_song(client_id, client_secret, redirect_uri, scope)
            current_track_id = new_track_id
            time.sleep(5)
        else:
            continue
            time.sleep(5)
    except spotipy.oauth2.SpotifyOauthError as error:
        auth(client_id, client_secret, redirect_uri, scope)
        time.sleep(5)
        print(f'spotify error {error}')
    except BaseException as error:
        print(error)   
        time.sleep(5) 
