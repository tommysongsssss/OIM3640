# You will need to import CSV and OS 

import csv
import os



def read_csv(filepath):
    """
    TODO: Read a CSV file and return the data in best format using csv module.
    """
    with open(filepath, "r", encoding="utf8", newline = "") as file:
        reader = csv.reader(file)
        data = list(reader)
        # data = file.read()  # read the file as one big string
        # data = file.readline()  # read the first line
        print(f"Number of rows: {len(data)}")
        print(f"Type of data: {type(data)}")
        print("Sample data preview:")
        print(data[:5]) 
    return data


def process_data(data):
    """Extract useful information from the raw data."""
    for line in data:
        # Process each line
        print(line)


def main():
    filepath = "/Users/thomassong0604/Documents/GitHub/OIM3640/CSV Portfolio"  # https://github.com/OIM3640/resources/blob/main/code/data/portfolio.csv
    if os.path.exists(filepath):
        data = read_csv(filepath)
        process_data(data)
    else:
        print(f"File not found: {filepath}")
    


if __name__ == "__main__":
    main()
