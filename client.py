import json
import socket


class Client:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def connect(self):
        try:
            msg = self.client.recv(1024).decode('utf-8')
            self.listen()
        except Exception as e:
            print(f'ERROR: {str(e)}')
            exit()

        if msg == 'YOU ARE CONNECTED!':
            self.listen()
        else:
            exit()

    def sender(self, text):
        self.client.send(text.encode('utf-8'))
        # пока не получим ответ, что сообщение принято посылаем запрос
        while self.client.recv(1024).decode('utf-8') != 'GETTED':
            self.client.send(text.encode('utf-8'))

    def listen(self):
        is_work = True
        while is_work:
            reqest = input('TYPE DATABASE REQUEST:')

            if reqest == 'disconnect':
                self.sender(reqest)
                print(self.client.recv(1024).decode('utf-8'))
            else:
                self.sender(reqest)
                data = json.loads(self.client.recv(1024).decode('utf-8'))

                if data['answer']:
                    print(f'SERVER ANSWER:\n\t{data["answer"]}')
                elif data['error']:
                    print(f'SERVER ANSWER:\n\t{data["error"]}')


client = Client('192.168.1.35', 5555)
client.connect()

