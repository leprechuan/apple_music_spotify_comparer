import unittest
from textwrap import dedent
from unittest.mock import mock_open, patch

import compare_apple_music_and_spotify as music_compare


class get_apple_music_data(unittest.TestCase):
    DATA = dedent("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Major Version</key><integer>1</integer>
	<key>Minor Version</key><integer>1</integer>
	<key>Date</key><date>2020-02-07T11:33:32Z</date>
	<key>Application Version</key><string>12.10.4.2</string>
	<key>Features</key><integer>5</integer>
	<key>Show Content Ratings</key><true/>
	<key>Music Folder</key><string>file://localhost/C:/Users/tobia/Music/iTunes/iTunes%20Media/</string>
	<key>Library Persistent ID</key><string>761DAB9727DA65A4</string>
	<key>Tracks</key>
	<dict>
		<key>3991</key>
		<dict>
			<key>Track ID</key><integer>3991</integer>
			<key>Name</key><string>Black Honey</string>
			<key>Artist</key><string>Thrice</string>
			<key>Album Artist</key><string>Thrice</string>
			<key>Album</key><string>To Be Everywhere Is to Be Nowhere</string>
			<key>Genre</key><string>Rock</string>
			<key>Kind</key><string>Apple Music AAC audio file</string>
			<key>Size</key><integer>8451545</integer>
			<key>Total Time</key><integer>239451</integer>
			<key>Disc Number</key><integer>1</integer>
			<key>Disc Count</key><integer>1</integer>
			<key>Track Number</key><integer>7</integer>
			<key>Track Count</key><integer>11</integer>
			<key>Year</key><integer>2016</integer>
			<key>Date Modified</key><date>2017-10-18T06:21:33Z</date>
			<key>Date Added</key><date>2017-10-18T06:21:33Z</date>
			<key>Bit Rate</key><integer>256</integer>
			<key>Sample Rate</key><integer>44100</integer>
			<key>Play Count</key><integer>42</integer>
			<key>Play Date</key><integer>3649468233</integer>
			<key>Play Date UTC</key><date>2019-08-24T03:10:33Z</date>
			<key>Release Date</key><date>2016-05-27T12:00:00Z</date>
			<key>Loved</key><true/>
			<key>Artwork Count</key><integer>1</integer>
			<key>Sort Album</key><string>To Be Everywhere Is to Be Nowhere</string>
			<key>Sort Artist</key><string>Thrice</string>
			<key>Sort Name</key><string>Black Honey</string>
			<key>Persistent ID</key><string>291EB79CF1586A1A</string>
			<key>Track Type</key><string>Remote</string>
			<key>Apple Music</key><true/>
		</dict>
	</dict>
	<key>Playlists</key>
	<array>
		<dict>
			<key>Name</key><string>Ny Musik</string>
			<key>Description</key><string></string>
			<key>Playlist ID</key><integer>10518</integer>
			<key>Playlist Persistent ID</key><string>74337AEBA9845B24</string>
			<key>All Items</key><true/>
			<key>Playlist Items</key>
			<array>
				<dict>
					<key>Track ID</key><integer>3991</integer>
				</dict>
			</array>
		</dict>
	</array>
</dict>
</plist>
""")

    @patch("builtins.open", mock_open(read_data=DATA))
    def test_open_file(self):
        result = music_compare.open_file("apple_music_library.xml")

        open.assert_called_once_with("apple_music_library.xml", "r")
        self.assertEqual(self.DATA, result)
        self.assertEqual("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Major Version</key><integer>1</integer>
	<key>Minor Version</key><integer>1</integer>
	<key>Date</key><date>2020-02-07T11:33:32Z</date>
	<key>Application Version</key><string>12.10.4.2</string>
	<key>Features</key><integer>5</integer>
	<key>Show Content Ratings</key><true/>
	<key>Music Folder</key><string>file://localhost/C:/Users/tobia/Music/iTunes/iTunes%20Media/</string>
	<key>Library Persistent ID</key><string>761DAB9727DA65A4</string>
	<key>Tracks</key>
	<dict>
		<key>3991</key>
		<dict>
			<key>Track ID</key><integer>3991</integer>
			<key>Name</key><string>Black Honey</string>
			<key>Artist</key><string>Thrice</string>
			<key>Album Artist</key><string>Thrice</string>
			<key>Album</key><string>To Be Everywhere Is to Be Nowhere</string>
			<key>Genre</key><string>Rock</string>
			<key>Kind</key><string>Apple Music AAC audio file</string>
			<key>Size</key><integer>8451545</integer>
			<key>Total Time</key><integer>239451</integer>
			<key>Disc Number</key><integer>1</integer>
			<key>Disc Count</key><integer>1</integer>
			<key>Track Number</key><integer>7</integer>
			<key>Track Count</key><integer>11</integer>
			<key>Year</key><integer>2016</integer>
			<key>Date Modified</key><date>2017-10-18T06:21:33Z</date>
			<key>Date Added</key><date>2017-10-18T06:21:33Z</date>
			<key>Bit Rate</key><integer>256</integer>
			<key>Sample Rate</key><integer>44100</integer>
			<key>Play Count</key><integer>42</integer>
			<key>Play Date</key><integer>3649468233</integer>
			<key>Play Date UTC</key><date>2019-08-24T03:10:33Z</date>
			<key>Release Date</key><date>2016-05-27T12:00:00Z</date>
			<key>Loved</key><true/>
			<key>Artwork Count</key><integer>1</integer>
			<key>Sort Album</key><string>To Be Everywhere Is to Be Nowhere</string>
			<key>Sort Artist</key><string>Thrice</string>
			<key>Sort Name</key><string>Black Honey</string>
			<key>Persistent ID</key><string>291EB79CF1586A1A</string>
			<key>Track Type</key><string>Remote</string>
			<key>Apple Music</key><true/>
		</dict>
	</dict>
	<key>Playlists</key>
	<array>
		<dict>
			<key>Name</key><string>Ny Musik</string>
			<key>Description</key><string></string>
			<key>Playlist ID</key><integer>10518</integer>
			<key>Playlist Persistent ID</key><string>74337AEBA9845B24</string>
			<key>All Items</key><true/>
			<key>Playlist Items</key>
			<array>
				<dict>
					<key>Track ID</key><integer>3991</integer>
				</dict>
			</array>
		</dict>
	</array>
</dict>
</plist>
""", result)

    def test_read_line_by_line(self):
        result = music_compare.open_file("apple_music_library.xml")
        self.assertEqual('''<?xml version="1.0" encoding="UTF-8"?>''',music_compare.read_line_by_line(self.DATA))