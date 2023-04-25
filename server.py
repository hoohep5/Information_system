import base64
import socket
import json
from cryptography.fernet import Fernet
from threading import Thread
import HashTable

ht = HashTable.HashTable(20)
ht = ht.load_from_file('HashUsers.txt')

class User:

    def __init__(self, name, password, ip, access_level):
        self.name = name
        self.password = password
        self.ip = ip
        self.access_level = access_level

    # открываем файл и читаем его построчно


with open('HashUsers.txt', 'r') as file:
    for line in file:
        # разделяем строку на поля
        fields = line.strip().split(';')




class Server:

    def __init__(self, ip, port):

        print(f"SERVER ip: {ip}\nSERVER port: {port}\n")
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(3)

        self.blocked = []
        self.users = []

    # load information about user from data.json to self.users[]
    def load(self):

        data = None

        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for ip in data:
            self.users.append(User(ip, data[ip][0], data[ip][1]))

    # service command
    def get_user(self, ip):

        for user in self.users:

            if user.ip == ip:
                return user

        return None

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
    def get_msg(user, key):

        data = user.recv(1024)
        f = Fernet(key)
        data = f.decrypt(data)

        return data.decode()

    # authorization user by password
    def authorization(user, addr):

        # Load users from file into a hash table
        ht = HashTable.HashTable(20)
        ht.load_from_file('users.txt')

        user_ip = addr[0]


        if user_ip in ht:
            user_data = ht.get(user_ip)
            user_level = user_data[0]
            user_password = user_data[1]

            if user_password != '':
                Server.sender(user, user_data[2], 'Type your password.')
                try:
                    user_password_input = Server.get_msg(user, user_data[2])
                except Exception as e:
                    user_password_input = None

                if user_password_input == user_password:
                    Server.sender(user, user_data[2], 'Access is allowed!')
                    Server.listen(user, addr)

                else:
                    Server.sender(user, user_data[2], 'Access denied!')
                    user.close()

            else:
                Server.sender(user, user_data[2], 'Access is allowed!')
                Server.listen(user, addr)

        else:
            Server.sender(user, user.key, 'Access denied!')
            user.close()


    def start_server(self):

        while True:
            # create individual for every user flow to authorization

            user, addr = self.ser.accept()
            Thread(target=self.authorization, args=(user, addr,)).start()

    def listen(self, user, addr):
        is_work = True
        while is_work:

            try:
                data = self.get_msg(user, self.get_user(addr[0]).key)
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

