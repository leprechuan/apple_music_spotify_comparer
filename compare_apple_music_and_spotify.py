import io

def main():
    print("Hello World!")

def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read()


def read_line_by_line(data):
    buf = io.StringIO(data)
    return buf.readline().strip()

if __name__ == "__main__":
    main()

