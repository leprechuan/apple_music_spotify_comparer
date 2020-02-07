def main():
    print("Hello World!")

def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read()

if __name__ == "__main__":
    main()

