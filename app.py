import eel
import spotipy

try:
    import spotipy
except ImportError:
    print("Error: spotipy library not found")

@eel.expose
def get_image_url():
    current_track = spotify_object.current_playback()
    # res = spotify_object.devices()
    # print(res)
    if current_track is not None and current_track["is_playing"]:
        current = spotify_object.currently_playing()
        if current is not None:
            artist = current["item"]["album"]["artists"][0]["name"]
            track = current["item"]["name"]
            album = current["item"]["album"]["name"]
            length = current["item"]["duration_ms"]
            progress = current["progress_ms"]
            album_art_url = current["item"]["album"]["images"][0]["url"]
            #print(album_art_url)

            # Create a dictionary with the desired values
            data = {
                "is_playing": True,
                "artist_name": artist,
                "song_title": track,
                "album_name": album,
                "length": length,
                "progress": progress,
                "album_art_url": album_art_url,
            }
        else:
            # Return a dictionary indicating that currently_playing() returned None
            data = {
                "is_playing": False,
                "error": "currently_playing() returned None"
            }
    else:
        # Return a dictionary indicating that music is not playing
        data = {
            "is_playing": False
        }

    # Return the dictionary
    return data
@eel.expose
def playerControl(functionSelect):
    # 1 = play pause
    # 2 = next track
    # 3 = previouse track
    # 4 = shuffle
    # 5 = repeat
    current_track = spotify_object.current_playback()
    match functionSelect:
        case 1: 
            if current_track is not None and current_track["is_playing"]:
                spotify_object.pause_playback()
                print("pause")
            elif current_track is not None and not current_track["is_playing"]:
                spotify_object.start_playback()
                print("start playback")
            else:
                print("playback failed")
        case 2:
            spotify_object.next_track()
            print("next")
        case 3:
            spotify_object.previous_track()
            print("previous")
        case 4:
            if current_track["shuffle_state"]:
                spotify_object.shuffle(False)
                print("shuffle false")
                eel.change_shuffle_colour(1)
            else:
                spotify_object.shuffle(True)
                print("shuffle true")
                eel.change_shuffle_colour(0)
        case 5:
            if current_track["repeat_state"] == "off" :
                spotify_object.repeat("context")
                eel.change_repeat_colour(1)
                print("repeat")
            else:
                spotify_object.repeat("off")
                eel.change_repeat_colour(0)
            

if __name__ == '__main__':
    SPOTIPY_CLIENT_ID = "0f90348c84d442aa8eb2390ac74d2c9e"
    SPOTIPY_CLIENT_SECRET = "22d1ed6eaf674162a08b6fc96a6815c5"
    SPOTIPY_REDIRECT_URI = "https://google.com"
    GENIUS_ACCESS_TOKEN = "Okbi1ioN5ofQ0P8B5XE2E9SUK7pU26cc8bvxsTIfRdlviikynk5elU_HSK4EDvCp"

    scope = "user-read-currently-playing user-read-playback-state user-modify-playback-state"

    oauth_object = spotipy.SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
    )
    token_dict = oauth_object.get_access_token()
    if token_dict is not None:
        token = token_dict["access_token"]
    # Spotify Object
    spotify_object = spotipy.Spotify(auth=token)


    eel.init('web', ['.html', '.css'])
    eel.start('index.html', size=(720, 720))
