#!/usr/bin/python3

import io
import re
import csv


class apple_music_data_parser():

    def __init__(self,file_name):
        self.file_name = file_name
        self.file_data = self.open_file()
        self.one_song_and_artist = {}
        self.all_songs_and_artists = []

    def open_file(self):
        with open(self.file_name, "r") as f:
            return f.read()


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




class spotify_data_parser():

    def __init__(self):
        self.all_songs_and_artists = []
        self.one_song_and_artist = {}

    def read_file(self,csvfile):
        with open(csvfile, "r" , newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return reader

    def is_artist(self,data):
        return "Artist Name" in data

    def is_song(self,data):
        return "Track Name" in data

    def save_artist(self,data):
       if self.is_artist(data):
           self.one_song_and_artist['Artist'] = data['Artist Name']

    def save_song(self,data):
       if self.is_song(data):
           self.one_song_and_artist['Song']=data['Track Name']

    def combine_song_and_artist(self):
        if self.one_song_and_artist.get('Song') != None and self.one_song_and_artist.get('Artist') != None:
            self.all_songs_and_artists.append(self.one_song_and_artist)

    def create(self, file_name):
        csv_formated_data=self.read_file(file_name)
        for row in csv_formated_data:
            self.save_song(row)
            self.save_artist(row)
            self.combine_song_and_artist()
            self.one_song_and_artist = {}