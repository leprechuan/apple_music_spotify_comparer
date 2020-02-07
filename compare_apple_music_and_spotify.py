import io
import re



class apple_music_data_parser():

    def __init__(self,file_name):
        self.file_name = file_name
        self.file_data = self.open_file()
        self.one_song_and_artist = {}
        self.all_songs_and_artists = []


    def open_file(self):
        with open(self.file_name, "r") as f:
            return f.read()


    def read_line_by_line(self):
        data=""
        buf = io.StringIO(self.file_data)
        for a in buf:
            data =data + a.strip()
        return data

    def is_artist(self, line):
        if "Artist" in line:
            return re.search(r'<string>(.*?)</string', line).group(1)

    def is_song(self, line):
        if "Name" in line:
            return re.search(r'<string>(.*?)</string', line).group(1)

    def save_song(self,Name):
        self.one_song_and_artist.update({'Song':Name})

    def save_if_artist(self,line):
        artist_name = self.is_artist(line)
        if artist_name:
            self.one_song_and_artist.update({'Artist':artist_name})

    def save_if_song(self,line):
        song = self.is_song(line)
        if song:
            self.one_song_and_artist.update({'Song':song})

    def save_song_and_artist(self):
        self.all_songs_and_artists.append(self.one_song_and_artist)
        self.one_song_and_artist={}

    def create(self):
        data = ""
        buf = io.StringIO(self.file_data)
        for a in buf:
            self.save_if_artist(a)
            self.save_if_song(a)
            if 'Artist' in self.one_song_and_artist and 'Song' in self.one_song_and_artist:
                self.save_song_and_artist()

        return self.all_songs_and_artists




