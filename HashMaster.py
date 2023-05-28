import hashlib

class HashMaster:

    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_key_function(self, key):
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size

    def save_in_file(self, filename):
        with open(filename, 'w') as f:
            for index in range(self.size):
                for pair in self.table[index]:
                    f.write(pair[0] + ';' + pair[1] + ';' + pair[2] + '\n')

    def get_master(self, key, procedure):
        index = self.hash_key_function(key)
        try:
            for pair in self.table[index]:
                if pair[0] == key and procedure == pair[1]:
                    print(self.table[index])
                else:
                    print('not found')
        except Exception as e:
            print('GET_PROCEDURE ERROR!')

    def insert(self, key, procedure, exp):
        index = self.hash_key_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = procedure
                pair[2] = exp
                return
        self.table[index].append([key, procedure, exp])
        self.save_in_file('HashMaster.txt')

    def display_table(self):
        for i in range(self.size):
            print(f"Bucket {i}:")
            for pair in self.table[i]:
                print(f"  {pair[0]}, Procedure: {pair[1]}, Exp: {pair[2]} ")

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
                    key, procedure, exp = line.strip().split(delimiter)
                    self.insert(key, procedure, exp)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    key, procedure, exp = line.strip().split(';')
                    self.insert(key, procedure, exp)

    def add_master(self, key, procedure, exp):
        self.insert(key, procedure, exp)

