import base64
import socket
from cryptography.fernet import Fernet
from threading import Thread
import HashTable

ht = HashTable.HashTable(20)
ht = ht.load_from_file('HashUsers.txt')

IP = 'localhost'  # адрес хоста
PORT = 8080  # порт для приема запросов


class User:

    def __init__(self, name, password, ip, access_level):
        self.name = name
        self.password = password
        self.ip = ip
        self.access_level = access_level

        secret_key = ''
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
    def sender(user, key, text):

        f = Fernet(key)

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
    def get_user(login):

        index = HashTable.hash_table.hash_key_function(login)

        try:

            for pair in HashTable.hash_table.table[index]:

                if pair[0] == login:
                    return HashTable.hash_table.table[index]

                else:
                    print('NON-EXISTENT USER!')

        except Exception as e:
            print('GET_USER ERROR!')

    # authorization user by password
    @staticmethod
    def authorization(self, user, addr):

        user_ip = addr[0]
        user_port = addr[1]

        # Load users from file into a hash table
        ht = HashTable.HashTable(20)
        ht.load_from_file('users.txt')

        this_user = list(self.get_user(user.name))

        password = this_user[1]
        ip = this_user[2]
        level = this_user[3]

        if password != '':
            Server.sender(user, secret_key, 'Type your password.')
            try:
                user_password_input = Server.get_msg(user, key)
            except Exception as e:
                user_password_input = None

            user_password = password.encode()
            if user_password_input == user_password:
                Server.sender(user, key, 'Access is allowed!')
                Server.listen(user, addr)

            else:
                Server.sender(user, key, 'Access denied!')
                user.close()

        else:
            Server.sender(user, key, 'Access is allowed!')
            Server.listen(user, addr)

    def start_server(self):

        while True:
            # create individual for every user flow to authorization

            user, addr = self.ser.accept()
            Thread(target=self.authorization, args=(user, addr)).start()



    def listen(self, user, addr):
        is_work = True
        while is_work:

            try:

                data = self.get_msg(user, self.get_user(addr[0]).secret_key)
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

                    this_user = self.get_user(addr[0])
                    if this_user:

                        if msg == 'get access level':
                            self.sender(user, this_user.key, this_user.level)

                        if msg == 'print hash table users':
                            with open('HashUsers.txt', 'r') as f:
                                read_file = f.read()
                                print(read_file)
