import json
import socket


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))

    def send_request(self, request_type, data):
        reqest = {
            'request_type': request_type,
            'data': data
        }
        json_request = json.dumps(reqest)
        self.client.sendall(json_request.encode('utf-8'))

        respon = b""
        while True:
            data = self.client.recv(1024)
            respon += data
            if len(data) < 1024:
                break

        return json.loads(respon)

    def authorization(self, keyy, passwordd):
        data = {
            'key': keyy,
            'password': passwordd
        }
        responsee = self.send_request('authorization', data)
        return responsee['answer']

    def database_request(self, request):
        responsee = self.send_request('database', request)
        return responsee['answer']


if __name__ == '__main__':
    client = Client('192.168.56.1', 5000)

    while True:
        command = input("Enter command: ")
        if command == "quit":
            break

        if command == "auth":
            key = input("Enter key: ")
            password = input("Enter password: ")
            access_level = client.authorization(key, password)
            print(f"Access level: {access_level}")

        if command == "database":
            req = input("Enter database request: ")
            response = client.database_request(req)
            print(f"Database response: {response}")
