import socket
import json

server_ip = '192.168.56.1'
server_port = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

response = client.recv(1024).decode('utf-8')
print(response)

while True:

    request_type = input('Введите Запрос: ')


    if request_type == 'authorization':
        key = input('Введите ключ: ')
        password = input('Введите пароль: ')
        data = {
            'request_type': request_type,
            'key': key,
            'password': password
        }

    elif request_type == 'regist':
        key = input('Введите время: ')
        procedure = input('Введите процедуру: ')
        master = input('Введите мастера: ')
        user = input('Введите имя: ')
        data = {
            'request_type': request_type,
            'key': key,
            'procedure': procedure,
            'master': master,
            'user': user
        }

    elif request_type == 'disconnect':
        client.send(request_type.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        break

    else:
        request = input('Введите запрос: ')
        data = {
            'request_type': request_type,
            'request': request
        }

    if request_type not in ['authorization', 'database', 'disconnect', 'regist']:
        print('Неверный тип запроса!')
        continue

    message = json.dumps(data)
    client.send(message.encode('utf-8'))

    response = client.recv(1024).decode('utf-8')
    print(response)

client.close()
