import unittest
from textwrap import dedent
from unittest.mock import mock_open, patch

import compare_apple_music_and_spotify as music_compare


class get_apple_music_data(unittest.TestCase):
    DATA_ONE_LINE= dedent("""<?xml version="1.0" encoding="UTF-8"?>""")

    DATA_SEVERAL_LINES = dedent("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">""")

    def setUp(self):
        self.apple_music_data_reader = music_compare.apple_music_data_reader("apple_music_library.xml")

    @patch("builtins.open", mock_open(read_data=DATA_ONE_LINE))
    def test_open_file(self):
        result = self.apple_music_data_reader.open_file()
        open.assert_called_once_with("apple_music_library.xml", "r")
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>""", result)

    @patch("builtins.open", mock_open(read_data=DATA_ONE_LINE))
    def test_one_line(self):
        self.apple_music_data_reader = music_compare.apple_music_data_reader("apple_music_library.xml")
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>''',self.apple_music_data_reader.read_line_by_line())

    @patch("builtins.open", mock_open(read_data=DATA_SEVERAL_LINES))
    def test_several_lines(self):
        self.apple_music_data_reader = music_compare.apple_music_data_reader("apple_music_library.xml")
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">''',self.apple_music_data_reader.read_line_by_line())


