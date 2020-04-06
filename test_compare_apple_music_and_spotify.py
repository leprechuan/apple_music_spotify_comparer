import tempfile
import unittest
from textwrap import dedent
from unittest.mock import mock_open, patch

import compare_apple_music_and_spotify as music_compare


class get_apple_music_data(unittest.TestCase):
    DATA_ONE_LINE= dedent("""<?xml version="1.0" encoding="UTF-8"?>""")

    DATA_SEVERAL_LINES = dedent("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">""")

    DATA_ONE_ARTIST = dedent("""<key>Artist</key><string>Drew Goddard</string>""")
    DATA_ONE_SONG = dedent("""<key>Name</key><string>The Cabin In the Woods</string>""")
    DATA_ONE_SONG_AND_ARTIST = dedent("""<key>Artist</key><string>Drew Goddard</string>
                                        <key>Name</key><string>The Cabin In the Woods</string>""")

    DATA_SEVERAL_ARTISTS_AND_SONGS = dedent('''<key>Name</key><string>The Cabin In the Woods</string>
    <key>Artist</key><string>Drew Goddard</string>
    <key>Name</key><string>Pulp Fiction</string>
	<key>Artist</key><string>Quentin Tarantino</string>''')

    def setUp(self):
        self.file = tempfile.NamedTemporaryFile(mode='w', delete=True)


    @patch("builtins.open", mock_open(read_data=DATA_ONE_LINE))
    def test_open_file(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser(self.file)
        result = self.apple_music_data_parser.file_data
        open.assert_called_once_with(self.file , "r")
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>""", result)

    @patch("builtins.open", mock_open(read_data=DATA_ONE_ARTIST))
    def test_save_one_artist_from_line(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser(self.file)
        self.apple_music_data_parser.create()
        self.assertEqual("Drew Goddard",self.apple_music_data_parser.one_song_and_artist.get('Artist'))

    @patch("builtins.open", mock_open(read_data=DATA_ONE_SONG))
    def test_save_one_song(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser(self.file)
        self.apple_music_data_parser.create()
        self.assertEqual("The Cabin In the Woods", self.apple_music_data_parser.one_song_and_artist.get('Song'))

    @patch("builtins.open", mock_open(read_data=DATA_ONE_SONG_AND_ARTIST))
    def test_save_one_song_and_artist(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser(self.file)
        self.apple_music_data_parser.create()
        self.assertEqual([{'Artist': "Drew Goddard",'Song':"The Cabin In the Woods"}],self.apple_music_data_parser.all_songs_and_artists)

    @patch("builtins.open", mock_open(read_data=DATA_SEVERAL_ARTISTS_AND_SONGS))
    def test_save_several_songs_and_artists(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser(self.file)
        self.apple_music_data_parser.create()
        self.assertEqual([{'Artist': "Drew Goddard",'Song':"The Cabin In the Woods"},{'Artist': "Quentin Tarantino",'Song':"Pulp Fiction"}],self.apple_music_data_parser.all_songs_and_artists)



class spotify_data_parser(unittest.TestCase):
    DATA_ONE_LINE = dedent("""﻿Spotify URI,Track Name,Artist Name,Album Name,Disc Number,Track Number,Track Duration (ms),Added By,Added At""")

    LINE_NO_ARTIST = dedent("""<key>Artist</key><string>Drew Goddard</string>""")

    def test_open_file_and_return_formated_data_split_by_coma(self):
        with patch("builtins.open", mock_open(read_data="split,by,")) as mock_file:
            result = music_compare.spotify_data_parser().read_file("/test_path")
            open.assert_called_once_with("/test_path", "r", newline='')
            self.assertTrue(result,"_csv.DictReader")

    def test_no_artist_found_on_line(self):
        lines_csv_dict_reader_formated = {
            "not found": "not important",
        }
        result= music_compare.spotify_data_parser().is_artist(lines_csv_dict_reader_formated)
        self.assertEqual(False,result)

    def test_artist_found_on_line(self):
        lines_csv_dict_reader_formated = {
            "Artist Name": "Avenged Sevenfold",
        }
        result= music_compare.spotify_data_parser().is_artist(lines_csv_dict_reader_formated)
        self.assertEqual(True,result)

    def test_song_not_found_on_line(self):
        lines_csv_dict_reader_formated = {
            "not found": "Nightmare",
        }
        result= music_compare.spotify_data_parser().is_song(lines_csv_dict_reader_formated)
        self.assertEqual(False,result)

    def test_song_found_on_line(self):
        lines_csv_dict_reader_formated = {
            "Track Name": "Nightmare",
        }
        result= music_compare.spotify_data_parser().is_song(lines_csv_dict_reader_formated)
        self.assertEqual(True,result)

    def test_dont_save_if_artist_not_found(self):
        lines_csv_dict_reader_formated = {
            "not found": "not important",
        }
        music_compare.spotify_data_parser().save_artist(lines_csv_dict_reader_formated)
        self.assertEqual({},music_compare.spotify_data_parser().one_song_and_artist)

    def test_save_if_artist_found(self):
        lines_csv_dict_reader_formated = {
            "Artist Name": "test_artist",
        }
        self.spotify_data_parser = music_compare.spotify_data_parser()
        self.spotify_data_parser.save_artist(lines_csv_dict_reader_formated)
        self.assertEqual('test_artist', self.spotify_data_parser.one_song_and_artist.get('Artist'))


    def test_dont_save_if_song_not_found(self):
        lines_csv_dict_reader_formated = {
            "not found": "not important",
        }
        music_compare.spotify_data_parser().save_song(lines_csv_dict_reader_formated)
        self.assertEqual({},music_compare.spotify_data_parser().one_song_and_artist)

    def test_save_if_song_found(self):
        lines_csv_dict_reader_formated = {
            "Track Name": "test_song",
        }
        self.spotify_data_parser = music_compare.spotify_data_parser()
        self.spotify_data_parser.save_song(lines_csv_dict_reader_formated)
        self.assertEqual('test_song', self.spotify_data_parser .one_song_and_artist.get('Song'))

    def test_combine_song_found_and_NOT_artist(self):
        lines_csv_dict_reader_formated = {
            "Name": "test_song",
            "Artist": "test_artist"
        }
        self.spotify_data_parser = music_compare.spotify_data_parser()
        self.spotify_data_parser.save_song(lines_csv_dict_reader_formated)

        self.spotify_data_parser.combine_song_and_artist()
        self.assertEqual([], self.spotify_data_parser.all_songs_and_artists)

    def test_combine_song_and_artist_if_found(self):
        lines_csv_dict_reader_formated = {
            "Track Name": "test_song",
            "Artist Name": "test_artist"
        }
        self.spotify_data_parser = music_compare.spotify_data_parser()
        self.spotify_data_parser.save_song(lines_csv_dict_reader_formated)
        self.spotify_data_parser.save_artist(lines_csv_dict_reader_formated)

        self.spotify_data_parser.combine_song_and_artist()
        self.assertEqual([{'Artist': 'test_artist', 'Song': 'test_song'}], self.spotify_data_parser.all_songs_and_artists)


    def test_combine_several_songs_and_artists(self):
        with patch("builtins.open", mock_open(read_data='''Spotify URI,Track Name,Artist Name,Album Name,Disc Number,Track Number,Track Duration (ms),Added By,Added At
"spotify:track:4UEo1b0wWrtHMC8bVqPiH8","Nightmare","Avenged Sevenfold","Nightmare","1","1","374453","spotify:user:","2010-10-17T20:18:40Z"
"spotify:track:1d5UuboIPRMD4HaU3yycKC","Somewhere I Belong","Linkin Park","Meteora (Bonus Edition)","1","3","213933","spotify:user:","2010-10-17T20:24:25Z"''')) as mock_file:
            self.spotify_data_parser = music_compare.spotify_data_parser()
            self.spotify_data_parser.create("/test_path")
        #self.spotify_data_parser.combine_song_and_artist()
        self.assertEqual([{'Artist': 'Avenged Sevenfold', 'Song': 'Nightmare'},{'Artist': 'Linkin Park', 'Song': 'Somewhere I Belong'}], self.spotify_data_parser.all_songs_and_artists)