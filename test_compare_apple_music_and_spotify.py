import tempfile
import unittest

from unittest.mock import mock_open, patch, MagicMock, call
import compare_apple_music_and_spotify as music_compare


class get_apple_music_data(unittest.TestCase):
    def test_open_file(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            apple_music_data_parser = music_compare.AppleMusicDataParser()
            apple_music_data_parser.create("/apple_music")
            assert open("/apple_music").read() == "data"
            mock_file.assert_called_with("/apple_music")

    def test_save_one_artist_from_line(self):
        with patch("builtins.open", mock_open(read_data="""<key>Artist</key><string>Drew Goddard</string>""")):
            apple_music_data_parser = music_compare.AppleMusicDataParser()
            apple_music_data_parser.create("/apple_music")
            self.assertEqual("Drew Goddard", apple_music_data_parser.one_song_and_artist.get('Artist'))

    def test_save_one_song(self):
        with patch("builtins.open", mock_open(read_data="""<key>Name</key><string>The Cabin In the Woods</string>""")):
            apple_music_data_parser = music_compare.AppleMusicDataParser()
            apple_music_data_parser.create("/apple_music")
            self.assertEqual("The Cabin In the Woods", apple_music_data_parser.one_song_and_artist.get('Song'))

    def test_save_one_song_and_artist(self):
        with patch("builtins.open", mock_open(read_data="""<key>Artist</key><string>Drew Goddard</string>
                                        <key>Name</key><string>The Cabin In the Woods</string>""")):
            apple_music_data_parser = music_compare.AppleMusicDataParser()
            apple_music_data_parser.create("/apple_music")
            self.assertEqual([{'Artist': "Drew Goddard", 'Song': "The Cabin In the Woods"}],
                             apple_music_data_parser.all_songs_and_artists)

    def test_save_several_songs_and_artists(self):
        with patch("builtins.open", mock_open(read_data='''<key>Name</key><string>The Cabin In the Woods</string>
    <key>Artist</key><string>Drew Goddard</string>
    <key>Name</key><string>Pulp Fiction</string>
	<key>Artist</key><string>Quentin Tarantino</string>''')):
            apple_music_data_parser = music_compare.AppleMusicDataParser()
            apple_music_data_parser.create("/apple_music")
        self.assertEqual([{'Artist': "Drew Goddard", 'Song': "The Cabin In the Woods"},
                          {'Artist': "Quentin Tarantino", 'Song': "Pulp Fiction"}],
                         apple_music_data_parser.all_songs_and_artists)



class spotify_data_parser(unittest.TestCase):

    def test_open_file_and_return_formated_data_split_by_coma(self):
        with patch("builtins.open", mock_open(read_data="split,by,")):
            result = music_compare.spotify_data_parser().read_file("/test_path")
            open.assert_called_once_with("/test_path", "r", newline='')
            self.assertTrue(result, "_csv.DictReader")

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
        self.assertEqual([{'Artist': 'test_artist', 'Song': 'test_song'}],
                         self.spotify_data_parser.all_songs_and_artists)

    def test_combine_several_songs_and_artists(self):
        with patch("builtins.open", mock_open(read_data='''Spotify URI,Track Name,Artist Name,Album Name,Disc Number,Track Number,Track Duration (ms),Added By,Added At
"spotify:track:4UEo1b0wWrtHMC8bVqPiH8","Nightmare","Avenged Sevenfold","Nightmare","1","1","374453","spotify:user:","2010-10-17T20:18:40Z"
"spotify:track:1d5UuboIPRMD4HaU3yycKC","Somewhere I Belong","Linkin Park","Meteora (Bonus Edition)","1","3","213933","spotify:user:","2010-10-17T20:24:25Z"''')) as mock_file:
            self.spotify_data_parser = music_compare.spotify_data_parser()
            self.spotify_data_parser.create("/test_path")
        self.assertEqual([{'Artist': 'Avenged Sevenfold', 'Song': 'Nightmare'},
                          {'Artist': 'Linkin Park', 'Song': 'Somewhere I Belong'}],
                         self.spotify_data_parser.all_songs_and_artists)


class apple_music_and_spotify_comparer(unittest.TestCase):

    def setUp(self):
        self.comparer = music_compare.apple_music_and_spotify_comparer()

    @patch.object(music_compare.spotify_data_parser, 'create')
    @patch.object(music_compare.AppleMusicDataParser, 'create')
    def test_save_data_from_spotify_and_apple_music_in_class(self, apple_music, spotify):
        test = music_compare.apple_music_and_spotify_comparer()
        spotify.return_value = [{'Artist': 'test_artist1', 'Song': 'test_song1'}]
        apple_music.return_value = [{'Artist': 'test_artist2', 'Song': 'test_song2'}]
        test.save_data_locally("/spotify", "/apple_music")
        self.assertEqual([{'Artist': 'test_artist1', 'Song': 'test_song1'}], test.spotify_lib)
        self.assertEqual([{'Artist': 'test_artist2', 'Song': 'test_song2'}], test.apple_music_lib)

    @patch.object(music_compare.spotify_data_parser, 'create')
    @patch.object(music_compare.AppleMusicDataParser, 'create')
    def test_print_song_and_artist_when_song_not_found_in_apple_music(self, apple_music, spotify):
        spotify.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                {'Artist': 'test_artist_no_match', 'Song': 'test_song_no_match'}]
        apple_music.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'}]
        with patch("builtins.print") as mock_print:
            self.comparer.find_matches("/spotify", "/apple_music")
            mock_print.assert_called_once_with(
                "song: test_song_no_match by artist: test_artist_no_match not found in apple music")

    @patch.object(music_compare.spotify_data_parser, 'create')
    @patch.object(music_compare.AppleMusicDataParser, 'create')
    def test_print_song_and_artist_when_song_not_found_in_spotify(self, apple_music, spotify):
        spotify.return_value = [{'Artist': 'test_artist_no_match', 'Song': 'test_song_no_match'}]
        apple_music.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                    {'Artist': 'test_artist_no_match', 'Song': 'test_song_no_match'}]
        with patch("builtins.print") as mock_print:
            self.comparer.find_matches("/spotify", "/apple_music")
            mock_print.assert_called_once_with("song: test_song by artist: test_artist not found in spotify")

    @patch.object(music_compare.spotify_data_parser, 'create')
    @patch.object(music_compare.AppleMusicDataParser, 'create')
    def test_print_several_songs_and_artists_when_song_not_found_in_apple_music(self, apple_music, spotify):
        spotify.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                {'Artist': 'test_artist_no_match', 'Song': 'test_song_no_match'},
                                {'Artist': 'test_artist_no_match2', 'Song': 'test_song_no_match2'},
                                {'Artist': 'test_artist2', 'Song': 'test_song2'}]
        apple_music.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                    {'Artist': 'test_artist2', 'Song': 'test_song2'}]
        with patch("builtins.print") as mock_print:
            self.comparer.find_matches("/spotify", "/apple_music")
            self.assertEqual(2, mock_print.call_count)
            mock_print.assert_has_calls(
                [call("song: test_song_no_match by artist: test_artist_no_match not found in apple music"),
                 call("song: test_song_no_match2 by artist: test_artist_no_match2 not found in apple music")],
                any_order=False)

    @patch.object(music_compare.spotify_data_parser, 'create')
    @patch.object(music_compare.AppleMusicDataParser, 'create')
    def test_print_several_songs_and_artists_when_song_not_found_in_spotify(self, apple_music, spotify):
        apple_music.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                    {'Artist': 'test_artist_no_match', 'Song': 'test_song_no_match'},
                                    {'Artist': 'test_artist_no_match2', 'Song': 'test_song_no_match2'},
                                    {'Artist': 'test_artist2', 'Song': 'test_song2'}]
        spotify.return_value = [{'Artist': 'test_artist', 'Song': 'test_song'},
                                {'Artist': 'test_artist2', 'Song': 'test_song2'}]
        with patch("builtins.print") as mock_print:
            self.comparer.find_matches("/spotify", "/apple_music")
            self.assertEqual(2, mock_print.call_count)
            mock_print.assert_has_calls(
                [call("song: test_song_no_match by artist: test_artist_no_match not found in spotify"),
                 call("song: test_song_no_match2 by artist: test_artist_no_match2 not found in spotify")],
                any_order=False)
