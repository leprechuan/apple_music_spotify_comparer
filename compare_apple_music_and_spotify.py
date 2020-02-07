import io

def main():
    print("Hello World!")

class apple_music_data_reader():

    def __init__(self,file_name):
        self.file_name = file_name
        self.file_data =self.open_file()


    def open_file(self):
        with open(self.file_name, "r") as f:
            return f.read()


    def read_line_by_line(self):
        data=""

        buf = io.StringIO(self.file_data)
        for a in buf:
            data =data + a.strip()
        return data

    def read_artist(self, line):
        if "Artist" in line:
            return "Drew Goddard"


    def read_song(self, line):
        if "Name" in line:
            return "Sounds of a Playground Fading"

if __name__ == "__main__":
    main()

