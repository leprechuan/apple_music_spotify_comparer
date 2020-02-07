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
        buf = io.StringIO(self.file_data)
        return buf.readline().strip()

if __name__ == "__main__":
    main()

