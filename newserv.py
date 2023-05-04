import json
import socket
from threading import Thread

import HashTable


class Server:

    def __init__(self, ip, port, hashtable):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(5)
        self.hash_table = hashtable

    def listen(self):
        while True:
            client_socket, client_address = self.server.accept()
            thread = Thread(target=self.client_handler, args=(client_socket, client_address))
            thread.start()

    def client_handler(self, client_socket, client_address):
        try:
            client_socket.send('YOU ARE CONNECTED!'.encode('utf-8'))

            while True:
                msg = client_socket.recv(1024).decode('utf-8')

                if msg == 'disconnect':
                    client_socket.send('DISCONNECTED!'.encode('utf-8'))
                    client_socket.close()
                    break

                data = json.loads(msg)

                if data['request_type'] == 'authorization':
                    key = data['key']
                    password = data['password']
                    ip_address = client_address[0]
                    access_level = self.hash_table.verify_user(key, password)
                    response = {'answer': access_level}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif data['request_type'] == 'database':
                    request = data['request']
                    result = self.hash_table.get_user(request, client_address[0])
                    response = {'answer': result}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                else:
                    client_socket.send('UNKNOWN REQUEST!'.encode('utf-8'))

        except Exception as e:
            print(f'ERROR: {str(e)}')
            client_socket.close()


if __name__ == '__main__':
    hash_table = HashTable.HashTable(10)
    hash_table.load_from_file('HashUsers.txt')
    server = Server('192.168.1.35', 8000, hash_table)
    server.listen()

