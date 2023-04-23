import hashlib


class HashTable:

    # initialize empty hash table
    def __init__(self, size):

        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_key_function(self, key):

        # using hash-function sha-256 to generate search index
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size

    @staticmethod
    def hash_pass_function(password):

        # using hash-function sha-256 to grnerate password hash
        return hashlib.sha256(password.encode()).hexdigest()

    # inserts a key and value into a hash table. If the key already exists, then updates the value.
    def insert(self, key, value):

        index = self.hash_key_function(key)

        for pair in self.table[index]:

            if pair[0] == key:
                pair[1] = value
                return

        self.table[index].append([key, value])

        self.save_in_file('HashUsers.txt')

    # print hash table
    def display_table(self):

        for i in range(self.size):
            print(f"Bucket {i}:")

            for pair in self.table[i]:
                print(f"  {pair[0]}: {pair[1]}")

    # searching element by key
    def search(self, key):

        index = self.hash_key_function(key)

        for pair in self.table[index]:

            if pair[0] == key:
                return pair[1]

        return None

    # load data from txt and hashing psswords
    def load_txt(self, filename, delimiter=';'):

        with open(filename, 'r') as f:

            for line in f:

                if line.strip():
                    key, password = line.strip().split(delimiter)
                    hashed_password = self.hash_pass_function(password)
                    self.insert(key, hashed_password)


    def load_from_file(self, filename):

        with open(filename, 'r') as f:

            for line in f:

                if line.strip():
                    key, hashed_password = line.strip().split(';')
                    self.insert(key, hashed_password)

    def save_in_file(self, filename):

        with open(filename, 'w') as f:

            for index in range(self.size):

                for pair in self.table[index]:
                    f.write(pair[0] + ';' + pair[1] + '\n')


    def add_user(self, key, password):

        hashed_password = self.hash_pass_function(password)
        self.insert(key, hashed_password)

    def verify_user(self, key, password):

        hashed_password = self.search(key)

        if hashed_password:
            return hashed_password == self.hash_pass_function(password)

        else:
            return False


hash_table = HashTable(10)

# load users from txt (delimiter is ';')
hash_table.load_txt('Users.txt', ';')

# add new user
hash_table.add_user('new_user', 'new_password')

# checking password
is_correct = hash_table.verify_user('vitalya', '1234')

if is_correct:
    print('Пароль верный')
else:
    print('Пароль неверный')



hash_table.display_table()
