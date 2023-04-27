import base64
import socket

from cryptography.fernet import Fernet

import HashTable


class User:
    def __init__(self, ip, level, password):
        self.ip = ip
        self.level = level
        self.password = password

        symbols = {
            '0': 'Q', '1': 'W', '2': 'E', '3': 'R', '4': 'T', '5': 'Y', '6': 'U', '7': 'I', '8': 'O', '9': 'P',
        }
        p = ip.replace('.', '')
        i = 0
        secret_key = ''
        while len(secret_key) != 32:
            secret_key = f'{secret_key}{symbols[p[i]]}'
            i += 1
            if i == len(p):
                i = 0
        secret_key = secret_key.encode()
        self.secret_key = base64.urlsafe_b64encode(secret_key)





class Server:

    def __init__(self, ip, port):

        print(f"SERVER ip: {ip}\nSERVER port: {port}\n")
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(3)

        self.blocked = []
        self.users = []

    # encrypt and send message from server to user
    @staticmethod
    def sender(user, secret_key, text):

        f = Fernet(secret_key)

        try:
            text = text.encode()
            user.send(f.encrypt(text))

        except Exception as e:
            print('CLIENT DISCONNECTED!')

    # get encrypted message from user and decrypt it
    @staticmethod
    def get_msg(user, secret_key):

        data = user.recv(1024)
        f = Fernet(secret_key)
        data = f.decrypt(data)

        return data.decode()

    # service command
    @staticmethod
    def get_user(key):

        index = HashTable.hash_table.hash_key_function(key)

        try:

            for pair in HashTable.hash_table.table[index]:

                if pair[0] == key:
                    return HashTable.hash_table.table[index]

                else:
                    print('NON-EXISTENT USER!')

        except Exception as e:
            print('GET_USER ERROR!')

    # authorization user by password
    @staticmethod
    def authorization(self, user, addr):

        # Load users from file into a hash table
        ht = HashTable.HashTable(20)
        ht.load_from_file('HashUsers.txt')

        user_data = None
        while user_data is None:

            self.sender(user, '', 'Type your name.')
            user_name = Server.get_msg(user, '')
            if user_name:
                user_data = self.get_user(ht.hash_key_function(user_name))

        password = user_data[1]
        ip = user_data[2]
        level = user_data[3]

        if password != '':
            Server.sender(user, '', 'Type your password.')
            try:
                user_password_input = Server.get_msg(user, user_data[2])
            except Exception as e:
                user_password_input = None

            if HashTable.HashTable.hash_pass_function(user_password_input) == password:
                Server.sender(user, user_data[2], 'Access is allowed!')
                Server.listen(user, addr)

            else:
                Server.sender(user, user_data[2], 'Access denied!')
                user.close()

        else:
            Server.sender(user, user_data[2], 'Access is allowed!')
            Server.listen(user, addr)

    @staticmethod
    def listen(user, addr):
        is_work = True
        while is_work:

            try:
                data = Server.get_msg(user, HashTable.hash_table.find(addr[0])[2])
            except Exception as e:
                print('CLIENT DISCONNECTED!')
                data = ''
                is_work = False

            if len(data) > 0:
                msg = data

                if msg in ('disconnect', 'exit'):
                    print('CLIENT DISCONNECTED!')
                    user.close()
                    is_work = False

                else:
                    # user message processing

                    this_user = HashTable.hash_table.find(addr[0])
                    if this_user:

                        if msg == 'get access level':
                            Server.sender(user, this_user[2], this_user[3])

                        if msg == 'print hash table users':

                            with open('HashUsers.txt', 'r') as f:

                                read_file = f.read()
                                print(read_file)
