import csv

class FileManager:
    """Handles all File I/O operations."""

    def __init__(self):
        pass

    def write_file(self, file_name, content):
        """Writes content to a new file, failing if the file already exists."""
        try:
            with open(file_name, "x") as file:
                file.writelines(content)
        except Exception as e:
            print(f"Could not write file: {e}")

    def read_file(self, file_name):
        """Reads and returns all lines from a file."""
        try:
            with open(file_name, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Could not read file: {e}")

    def append_file(self, file_name, content):
        """Appends content to an existing file."""
        try:
            with open(file_name, "a") as file:
                file.writelines(content)
        except Exception as e:
            print(f"Could not append to file: {e}")

    def print_file(self, file_name):
        """Prints each line of a file to the console."""
        try:
            with open(file_name, "r") as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Could not read file: {e}")

    def read_csv(self, file_name):
        """Reads a CSV file :)"""
        data = []
        try:
            with open(file_name, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    data.append(row)

            return data

        except Exception as e:
            print(f"Could not read file: {e}")
            return data
