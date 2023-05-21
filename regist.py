import hashlib

class Regist:

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

    def get_regist(self, key):
        index = self.hash_key_function(key)
        try:
            for pair in self.table[index]:
                if pair[0] == key:
                    print(self.table[index])
                else:
                    print('not found')
        except Exception as e:
            print('GET_PROCEDURE ERROR!')

    def insert(self, key, user, procedure, master):
        index = self.hash_key_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = user
                pair[2] = procedure
                pair[3] = master
                return
        self.table[index].append([key, user, procedure, master])
        self.save_in_file('regist.txt')

    def display_table(self):
        for i in range(self.size):
            print(f"Bucket {i}:")
            for pair in self.table[i]:
                print(f"  {pair[0]} - {pair[1]}:, Procedure: {pair[2]}, Master: {pair[3]} ")

    def search(self, key):
        index = self.hash_key_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return True
        return False

    def load_txt(self, filename, delimiter=';'):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    key, user, procedure, master = line.strip().split(delimiter)
                    self.insert(key, user, procedure, master)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.strip():
                    key, user, procedure, exp = line.strip().split(';')
                    self.insert(key, user, procedure, exp)

    def add_regist(self, key, user, procedure, master):
        if(self.search(key)):
            text = "Время занято"
            return text
        else:
            self.insert(key, user, procedure, master)
            text = "Зарегестриравано"
            return text

