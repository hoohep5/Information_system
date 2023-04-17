import socket
import json

class Server:

    def __init__(self, ip, port):
        print(f"SERVER ip: {ip}\nSERVER port: {port}\n")
        self.ser = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(3)

    def sender(self, user, text):
        user.send(text.encode('utf-8'))

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            print(f'CONNECTED:\n\tIP: {addr[0]}\nPORT: {addr[1]}\n')
            self.listen()

    def listen(self, user):
        self.sender(user, "YOU ARE CONNECTED!")
        is_work = True
        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, "GETTED")

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


            

