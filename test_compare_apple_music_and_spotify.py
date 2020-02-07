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
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")

    @patch("builtins.open", mock_open(read_data=DATA_ONE_LINE))
    def test_open_file(self):
        result = self.apple_music_data_parser.open_file()
        open.assert_called_once_with("apple_music_library.xml", "r")
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>""", result)

    @patch("builtins.open", mock_open(read_data=DATA_ONE_LINE))
    def test_read_one_line(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>''',self.apple_music_data_parser.read_line_by_line())

    @patch("builtins.open", mock_open(read_data=DATA_SEVERAL_LINES))
    def test_read_several_lines(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">''',self.apple_music_data_parser.read_line_by_line())

    @patch("builtins.open", mock_open(read_data=DATA_ONE_ARTIST))
    def test_save_one_artist_from_line(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.apple_music_data_parser.create()
        self.assertEqual("Drew Goddard",self.apple_music_data_parser.one_song_and_artist.get('Artist'))

    @patch("builtins.open", mock_open(read_data=DATA_ONE_SONG))
    def test_save_one_song(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.apple_music_data_parser.create()
        self.assertEqual("The Cabin In the Woods", self.apple_music_data_parser.one_song_and_artist.get('Song'))

    @patch("builtins.open", mock_open(read_data=DATA_ONE_SONG_AND_ARTIST))
    def test_save_one_song_and_artist(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.apple_music_data_parser.create()
        self.assertEqual([{'Artist': "Drew Goddard",'Song':"The Cabin In the Woods"}],self.apple_music_data_parser.all_songs_and_artists)

    @patch("builtins.open", mock_open(read_data=DATA_SEVERAL_ARTISTS_AND_SONGS))
    def test_save_several_songs_and_artists(self):
        self.apple_music_data_parser = music_compare.apple_music_data_parser("apple_music_library.xml")
        self.apple_music_data_parser.create()
        self.assertEqual([{'Artist': "Drew Goddard",'Song':"The Cabin In the Woods"},{'Artist': "Quentin Tarantino",'Song':"Pulp Fiction"}],self.apple_music_data_parser.all_songs_and_artists)

    #def test_lines_no_artist_or_Song(self):


class spotify_data_parser(unittest.TestCase):

    def test_open_file(self):
        self.spotify_data_parser = music_compare.spotify_data_parser()