from scrapper import MetaSput
from spotify import Spotify

meta_sput = MetaSput()
# sput_artist, sput_album = meta_sput.sputnik(2017)
# meta_artist, meta_album = meta_sput.metacritic(2017)

# Combines the lists
albums_2017, artist_2017 = meta_sput.combined_list(meta_sput.sputnik(2017), meta_sput.metacritic(2017))

spotify_methods = Spotify()
# remember defining the class first like above,
# will instance it and will prevent self keyword errors

# This will create and add the tracks to a playlist
# spotify_methods.spotify(albums_2017, artist_2017, 2017)

# This will get playlist tracks
music_in_playlist = spotify_methods.get_spotify_playlist_tracks("2017")

# returns list of tracks not in Spotify platlist, could be syntax issues or other.
spotify_methods.left_over_albums(artist_2017, albums_2017, music_in_playlist)

# get track info to play. A test for a future app idea
song_id = spotify_methods.get_track_info("invent animate", "heavener")

# Track playback, will need to have an instance of Spotify playing.
spotify_methods.playback_song(song_id)
