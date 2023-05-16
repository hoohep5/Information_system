import socket
import json

server_ip = '192.168.56.1'
server_port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

response = client.recv(1024).decode('utf-8')
print(response)

while True:
    message = input('Введите сообщение: ')

    if message == 'disconnect':
        client.send(message.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        break

    request_type = input('Введите тип запроса (authorization/database): ')

    if request_type not in ['authorization', 'database']:
        print('Неверный тип запроса!')
        continue

    if request_type == 'authorization':
        key = input('Введите ключ: ')
        password = input('Введите пароль: ')
        data = {
            'request_type': request_type,
            'key': key,
            'password': password
        }
    else:
        request = input('Введите запрос: ')
        data = {
            'request_type': request_type,
            'request': request
        }

    message = json.dumps(data)
    client.send(message.encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    print(response)

client.close()
