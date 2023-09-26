import os
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


class Spotify:

    dotenv_path = 'secrets.env'
    load_dotenv(dotenv_path)

    # def __init__(self, dotenv_path):
    #     self.dotenv_path = 'secrets.env'
    #     load_dotenv(self.dotenv_path)
    # for dealing with ENVs on my machine.

    def spotify(self, albums, artists, year):

        # authorization
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        scope = 'playlist-modify-private'

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, show_dialog=True, scope=scope,
                                      redirect_uri="http://example.com", cache_path="token.txt"))
        # creates playlist
        user_id = sp.current_user()['id']
        playlist_name = year
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

        # Looping through albums to get tracks and adds to playlist
        for album, artist in zip(albums, artists):

            search_results = sp.search(f"album:{album} artist:{artist}", 50, 0, type='album')
            try:
                album_id = search_results['albums']['items'][0]['id']
                tracks_on_album = sp.album_tracks(album_id=album_id, limit=50)['items']
                tracks = []
                for song in tracks_on_album:
                    tracks.append(song['uri'])
                sp.playlist_add_items(playlist_id=playlist['id'], items=tracks)
            except IndexError:
                print(f"Something wrong with entry {album} by {artist}, either syntax-error, or album not available")


    def get_spotify_playlist_tracks(self, playlist_name):

        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        scope = 'playlist-read-private'
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, show_dialog=True, scope=scope,
                                      redirect_uri="http://example.com", cache_path="token.txt"))
        # current_user_playlist stopped working for some godforsaken reason.
        # Even though the user's playlist isn't high. It's not making too many api calls either, it's a spotity issue.
        # limit to 20 or it'll keep refresh to find the playlist.
        search_playlist = sp.current_user_playlists(limit=20)
        music_in_playlist = []
        offset = 0

        for year in search_playlist['items']:
            if year['name'] == playlist_name:
                play_id = year['id']
                break

        for x in range(140):
            playlist_items = sp.playlist_items(playlist_id=play_id, offset=offset, limit=50)
            offset += 50

            for i in range(50):
                try:
                    album_name = playlist_items['items'][i]['track']['album']['name']
                    artist_name = playlist_items['items'][i]['track']['album']['artists'][0]['name']
                    music_in_playlist.append(f"{artist_name} - {album_name}")

                except IndexError:
                    break
        # turn list into set to get rid of duplicates and then use sorted(list) to order and turn back into list.
        # set() doesn't work outside variable like I thought for some reason when it worked before.
        music_in_playlist = sorted(list(set(music_in_playlist)))
        return music_in_playlist

    def left_over_albums(self, artist_year, album_year, music_in_playlist_currently):
        not_on_spotify = []
        all_music_list = []
        for (artist_year, album_year) in zip(artist_year, album_year):
            artist_and_album = f"{artist_year} - {album_year}"
            all_music_list.append(artist_and_album)

        all_music_list = sorted(list(set(all_music_list)))

        for item in all_music_list:
            if item in music_in_playlist_currently:
                pass
            else:
                not_on_spotify.append(item)

        with open('left_over_albums.txt', 'w', encoding="utf-8") as file:
            for item in not_on_spotify:
                file.write(f"{item}\n")


    # left_over_albums(artist_2017, albums_2017, music_on_2017_playlist)

    # below are just playback test for a future project.

    # get a song_id.
    def get_track_info(self, artist, track, *args):

        # authorization
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        print(client_id)

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, show_dialog=True,
                                      redirect_uri="http://example.com", cache_path="token.txt"))

        search_params = f"artist:{artist} track:{track}"
        new_params = []
        for extra in args:
            new_params.append("".join(extra))
        for item in new_params:
            search_params += " " + item
        extra_params = len(args)
        if extra_params > 0:
            # search_for_song = sp.search(f"artist:{artist} track:{track}" + f"{str(args)}")
            search_for_song = sp.search(search_params)
            print(search_for_song)
        else:
            search_for_song = sp.search(f"artist:{artist} track:{track}")
        # print(search_for_song['tracks']['items'][0]['artists'][0]['name'])
        # print(search_for_song['tracks']['items'][0]['name'])
        # print(search_for_song['tracks']['items'][0]['album']['name'])
        # print(search_for_song['tracks']['items'][0]['uri'])
        uri = search_for_song['tracks']['items'][0]['uri']
        return uri


# make sure arguments are strings, if you want to add extra search terms like year, make sure they are a string and
# in the year: format
# both below works.
# song_id = get_track_info("invent animate", "heavener")
# song_id =  get_track_info("trophy eyes", "chlorine", 'album:chemical miracle', 'year:2016')


# playback test - successful and it sends a signal to play from the spotify app on my computer

    def playback_song(self, song_id):

        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        scope = "user-read-playback-state,user-modify-playback-state"

        # for playback add scope to the params
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, scope=scope, show_dialog=True,
                                      redirect_uri="http://example.com", cache_path="token.txt"))

        res = sp.devices()
        pprint(res)

        sp.start_playback(uris=[song_id])


    # playback_song(song_id)
