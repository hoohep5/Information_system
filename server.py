import json
import socket
from threading import Thread

import HashMaster
import HashProcedure
import HashTable
import regist


class Server:

    def __init__(self, ip, port, hashtable, regist, master, procedure):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(1)
        self.hash_table = hashtable
        self.regist = regist
        self.master = master
        self.procedure = procedure

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
                    access_level = self.hash_table.verify_user(key, password)
                    response = {access_level}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif data['request_type'] == 'database':
                    request = data['request']
                    result = self.hash_table.get_user(request, client_address[0])
                    response = {result}
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif data['request_type'] == 'procedures':
                    key = self.procedure.display_table
                    response = {
                        'key': key
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))

                elif data['request_type'] == 'regist':
                    key = data['key']
                    procedure = data['procedure']
                    master = data['master']
                    user = data['user']
                    result = self.regist.add_regist(key, user, procedure, master)
                    if (result == True):
                        response = {f'Time is full': result}
                        client_socket.send(json.dumps(response).encode('utf-8'))
                    elif (result == False):
                        response = {f'Register': result}
                        client_socket.send(json.dumps(response).encode('utf-8'))


        except Exception as e:
            print(f'ERROR: {str(e)}')
            client_socket.close()


if __name__ == '__main__':
    hash_table = HashTable.HashTable(10)
    regist_base = regist.Regist(10)
    hash_master = HashMaster.HashMaster(10)
    hash_Procedure = HashProcedure.HashProcedure(10)
    hash_table.load_from_file('HashUsers.txt')
    regist_base.load_from_file('regist.txt')
    hash_master.load_from_file('HashMaster.txt')
    hash_Procedure.load_from_file('HashProcedure.txt')
#    server = Server('10.23.11.49', 5000, hash_table, regist_base)
    server = Server('127.0.0.1', 2000, hash_table, regist_base, hash_master, hash_Procedure)
    server.listen()

