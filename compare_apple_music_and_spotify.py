#!/usr/bin/python3

import io
import re
import csv


class AppleMusicDataParser:

    def __init__(self):
        self.one_song_and_artist = {}
        self.all_songs_and_artists = []

    def read_file_data(self, file_name):
        with open(file_name, "r") as f:
            return f.read()

    def is_artist(self, line):
        if "Artist" in line:
            return re.search(r'<string>(.*?)</string', line).group(1)

    def is_song(self, line):
        if "Name" in line:
            return re.search(r'<string>(.*?)</string', line).group(1)

    def save_song(self, Name):
        self.one_song_and_artist.update({'Song': Name})

    def save_if_artist(self, line):
        artist_name = self.is_artist(line)
        if artist_name:
            self.one_song_and_artist.update({'Artist': artist_name})

    def save_if_song(self, line):
        song = self.is_song(line)
        if song:
            self.one_song_and_artist.update({'Song': song})

    def save_song_and_artist(self):
        self.all_songs_and_artists.append(self.one_song_and_artist)
        self.one_song_and_artist = {}

    def create(self, file_path):
        data = ""
        buf = io.StringIO(self.read_file_data(file_path))
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

    def read_file(self, csvfile):
        with open(csvfile, "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return reader

    def is_artist(self, data):
        return "Artist Name" in data

    def is_song(self, data):
        return "Track Name" in data

    def save_artist(self, data):
        if self.is_artist(data):
            self.one_song_and_artist['Artist'] = data['Artist Name']

    def save_song(self, data):
        if self.is_song(data):
            self.one_song_and_artist['Song'] = data['Track Name']

    def combine_song_and_artist(self):
        if self.one_song_and_artist.get('Song') != None and self.one_song_and_artist.get('Artist') != None:
            self.all_songs_and_artists.append(self.one_song_and_artist)

    def create(self, file_name):
        csv_formated_data = self.read_file(file_name)
        for row in csv_formated_data:
            self.save_song(row)
            self.save_artist(row)
            self.combine_song_and_artist()
            self.one_song_and_artist = {}
        return self.all_songs_and_artists


class apple_music_and_spotify_comparer():
    def __init__(self):
        self.spotify_lib = []
        self.apple_music_lib = []
        self.missing_in_apple_music = []
        self.missing_in_spotify = []

    def save_data_locally(self, spofity_path, apple_music_path):
        self.spotify_lib = spotify_data_parser().create(spofity_path)
        self.apple_music_lib = AppleMusicDataParser().create(apple_music_path)

    def is_in_apple_music(self, spotify_song):
        return self.match_found(self.apple_music_lib, spotify_song)

    def is_in_spotify(self, apple_music_song):
        return self.match_found(self.spotify_lib, apple_music_song)

    def match_found(self, lib, song):
        for a in lib:
            if all(item in a.items() for item in song.items()) is True:
                return True
        return False

    def find_matches(self, spotify_path, apple_music_path):
        self.save_data_locally(spotify_path, apple_music_path)
        for one_song in self.apple_music_lib:
            if self.is_in_spotify(one_song) is False:
                self.missing_in_spotify.append(one_song)

                # print("song: " + one_song['Song'] + " by artist: " + one_song['Artist'] + " not found in spotify")

        for one_song in self.spotify_lib:
            if self.is_in_apple_music(one_song) is False:
                self.missing_in_apple_music.append(one_song)
                # print("song: " + one_song['Song'] + " by artist: " + one_song['Artist'] + " not found in apple music")

        self.print_missing_spotify()
        self.print_missing_apple_music()

    def print_missing_spotify(self):
        if self.missing_in_spotify:
            print("following songs not found in spotify:")
            for a in self.missing_in_spotify:
                print(a['Song'] + " by artist " + a['Artist'])
            print()

    def print_missing_apple_music(self):
        if self.missing_in_apple_music:
            print("following songs not found in apple_music:")
            for a in self.missing_in_apple_music:
                print(a['Song'] + " by artist " + a['Artist'])
