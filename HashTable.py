import hashlib
# если хешированое имя есть в таблице, то мы переходим к нему и сотрим еще и на пароль, подавать надо логин и пароль


class HashTable:

    # initialize empty hash table
    def __init__(self, size):

        self.size = size
        # list of lists [ [   ], [   ], [   ] ]
        self.table = [[] for _ in range(size)]

    def hash_key_function(self, key):

        # using hash-function sha-256 to generate search index
        return int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size

    @staticmethod
    def hash_pass_function(password):

        # using hash-function sha-256 to generate password hash
        return hashlib.sha256(password.encode()).hexdigest()

    def save_in_file(self, filename):

        with open(filename, 'w') as f:
            for index in range(self.size):
                for pair in self.table[index]:
                    f.write(pair[0] + ';' + pair[1] + ';' + pair[2] + ';' + pair[3] + '\n')


    def get_user(self, key, ip):

        index = self.hash_key_function(key)

        try:

            for pair in self.table[index]:

                if pair[0] == key and ip == pair[2]:
                    print(self.table[index])

                else:
                    print('net takogo')

        except Exception as e:
            print('GET_USER ERROR!')

    # inserts a key and value into a hash table. If the key already exists, then updates the value.
    def insert(self, key, value, ip_address, access_level):

        index = self.hash_key_function(key)

        for pair in self.table[index]:

            if pair[0] == key:
                pair[1] = value
                pair[2] = ip_address
                pair[3] = access_level
                return

        self.table[index].append([key, value, ip_address, access_level])

        self.save_in_file('HashUsers.txt')
    # print hash table

    def display_table(self):

        for i in range(self.size):
            print(f"Bucket {i}:")

            for pair in self.table[i]:
                print(f"  {pair[0]}: {pair[1]}, IP: {pair[2]}, ACCESS: {pair[3]} ")
    # searching element by key

    def search(self, key):

        index = self.hash_key_function(key)

        for pair in self.table[index]:

            if pair[0] == key:
                return pair[1]

        return None
    # load data from txt and hashing passwords

    def load_txt(self, filename, delimiter=';'):

        with open(filename, 'r') as f:

            for line in f:

                if line.strip():
                    key, password, ip_address, access_level = line.strip().split(delimiter)
                    hashed_password = self.hash_pass_function(password)
                    self.insert(key, hashed_password, ip_address, access_level)

    def load_from_file(self, filename):

        with open(filename, 'r') as f:

            for line in f:

                if line.strip():
                    key, hashed_password, ip_address, access_level = line.strip().split(';')
                    self.insert(key, hashed_password, ip_address, access_level)

    def add_user(self, key, password, ip_address, access_level):

        hashed_password = self.hash_pass_function(password)
        self.insert(key, hashed_password, ip_address, access_level)

    def verify_user(self, key, password):

        hashed_password = self.search(key)

        if hashed_password:
            return hashed_password == self.hash_pass_function(password)

        else:
            return False


# hash_table = HashTable(10)
#
# load users from txt (delimiter is ';')
# hash_table.load_txt('Users.txt', ';')
#
# # add new user
# hashtable.add_user('new_user', 'new_password', '192.168.0.1', 'low')
#
# # checking password
# is_correct = hashtable.verify_user('vitalya', '1234')
#
# if is_correct:
#     print('Пароль верный')
# else:
#     print('Пароль неверный')
#
# hash_table.display_table()
#
# hash_table.get_user('vitalya', '6543.2345.543.2')


