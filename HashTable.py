import csv

# reading data from file


class HashTable:

    def __init__(self, filename):
        self.load_csv(filename)
        self.data = {}

    def load_csv(self, filename):
        # reading data from file

        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                key = row[0]
                value = row[1:]
                self.data[key] = value

