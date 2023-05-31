import socket
import json
import windows

#server_ip = '10.23.11.49'
#server_port = 5000
server_ip = '127.0.0.1'
server_port = 2000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))
response = client.recv(1024).decode('utf-8')

if response == 'YOU ARE CONNECTED!':

    while True:
        windows.Window.print_welcome(20, 3)
        request_type = input('Введите Запрос: ')


        if request_type == 'authorization':
            windows.Window.print_sign_in(30, 6)
            key = input('Введите логин: ')
            password = input('Введите пароль: ')
            data = {
                'request_type': request_type,
                'key': key,
                'password': password
            }

        elif request_type == 'procedures':
            data = {
                'request_type': request_type
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
            data = {}
            windows.Window.print_input_error(20, 3)

        message = json.dumps(data)
        client.send(message.encode('utf-8'))
        print(response)


else:
    windows.Window.print_connection_error(30, 6)
