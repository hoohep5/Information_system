import hashlib

class HashProcedure:

    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_key_function(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size

    def save_in_file(self, filename):
        with open(filename, 'w') as f:
            for index in range(self.size):
                for pair in self.table[index]:
                    f.write(pair[0] + ';' + pair[1] + ';' + pair[2] + ';' + pair[3] + '\n')

    def get_procedure(self, key, price):
        index = self.hash_key_function(key)
        try:
            for pair in self.table[index]:
                if pair[0] == key and price == pair[2]:
                    print(self.table[index])
                else:
                    print('not found')
        except Exception as e:
            print('GET_PROCEDURE ERROR!')

    def insert(self, key, about, price, time):
        index = self.hash_key_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = about
                pair[2] = price
                pair[3] = time
                return
        self.table[index].append([key, about, price, time])
        self.save_in_file('HashProcedure.txt')

    def display_table(self):
        for i in range(self.size):
            print(f"Bucket {i}:")
            for pair in self.table[i]:
                print(f"  {pair[0]}: {pair[1]}, Price: {pair[2]}, Time: {pair[3]} ")

    def search(self, key):
        index = self.hash_key_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None

    def load_txt(self, filename, delimiter=';'):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    key, about, price, time = line.strip().split(delimiter)
                    self.insert(key, about, price, time)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    key, about, price, time = line.strip().split(';')
                    self.insert(key, about, price, time)

    def add_procedure(self, key, about, price, time):
        self.insert(key, about, price, time)
