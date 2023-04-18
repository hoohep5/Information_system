import base64
import socket
import json
from cryptography.fernet import Fernet


class User:
    def __init__(self, ip, level, password):
        self.ip = ip
        self.level = level
        self.password = password

        key = ''
        symbols = {
            '0': 'Q', '1': 'W', '2': 'E', '3': 'R', '4': 'T', '5': 'Y', '6': 'U', '7': 'I', '8': 'O', '9': 'P',
        }
        p = ip.replace('.', '')
        i = 0
        key = ''
        while len(key) != 32:
            key = f'{key}{symbols[p[i]]}'
            i += 1
            if i == len(p):
                i = 0
        key = key.encode()
        self.key = base64.urlsafe_b64encode(key)


class Server:

    def __init__(self, ip, port):

        print(f"SERVER ip: {ip}\nSERVER port: {port}\n")
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(3)

        self.blocked = []
        self.users = []

    # save information about user to file data.json
    def save(self):

        data = {}

        for user in self.users:
            data.update({user.ip: [user.level, user.password]})

        data = json.dumps(data)
        data = json.loads(str(data))

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ident=4)

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
    def sender(self, user, key, text):

        f = Fernet(key)

        try:
            text = text.encode()
            user.send(f.encrypt(text))

        except Exception as e:
            print('CLIENT DISCONNECTED!')

    # get encrypted message from user and decrypt it
    def get_msg(self, user, key):

        data = user.recv(1024)
        f = Fernet(key)
        data = f.decrypt(data)

        return data.decode()

    # authorization user by password
    def authorization(self, user, addr):

        user_ip = addr[0]
        user_port = addr[1]

        if not (user_ip in self.blocked):  # Если пользователь не заблокирован

            this_user = self.get_user(addr[0])

            if this_user == None:
                self.users.append(User(addr[0], 'low level user', '1234pass')) # standart pass for user
                self.save()
                this_user = self.get_user(addr[0])

            if this_user.password != '':
                self.sender(user, this_user.key, 'Type you password.')
                try:
                    user_password = self.get_msg(user, this_user.key)
                except Exception as e:
                    user_password = None

                if user_password == this_user.password:
                    self.sender(user, this_user.key, 'Access is allowed!')
                    self.listen(user, addr)

                else:
                    self.sender(user, this_user.key, 'Access denied!')
                    user.close()

            else:
                self.sender(user, this_user.key, 'Access is allowed!')
                self.listen(user, addr)

        else:
            self.sender(user, user.key, 'Access denied!')
            user.close()


    def start_server(self):

        while True:

            user, addr = self.ser.accept()
            print(f'CONNECTED\n\tIP: {addr[0]}\nPORT: {addr[1]}\n')
            self.listen(user)

    def listen(self, user, addr):
        self.sender(user, user.key, "YOU ARE CONNECTED!")
        is_work = True
        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, user.key, "GETTED")

            except Exception as e:
                data = ''
                is_work = False

            if len(data) > 0:
                msg = data.decode('utf-8')
                if msg == 'DISCONNECT':
                    self.sender(user, "YOU ARE DISCONNECTED")
                    user.close()
                    is_work = False

                else:
                    file_database = open("database.txt", "r+")
                    database_content = file_database.read()

                    try:
                        answer = [x for x in data]
                        error = ''
                    except Exception as e:
                        error = str(e)
                        answer = ''
                    file_database.close()
                    self.sender(user, database_content)

                    ans = json.dumps({'answer': answer, 'error': error})

                    self.sender(user, ans)

            else:
                print('CLIENT DISCONNECTED')
                is_work = False
