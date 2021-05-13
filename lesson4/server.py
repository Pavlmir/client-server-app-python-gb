"""
Урок 3. Основы сетевого программирования
1. Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
a. клиент отправляет запрос серверу;
b. сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.
Функции сервера:
1. Принимает сообщение клиента;
2. Формирует ответ клиенту;
3. Отправляет ответ клиенту.
Имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
import sys
import json
from config import ACTION, PRESENCE, TIME, RESPONSE, OK, WRONG_REQUEST, ERROR, server_port, server_address
import socket


def check_correct_presence_and_response(presence_message):
    if ACTION in presence_message and \
            presence_message[ACTION] == PRESENCE and \
            TIME in presence_message and \
            isinstance(presence_message[TIME], float):
        return {RESPONSE: OK}
    else:
        return {RESPONSE: WRONG_REQUEST, ERROR: 'Не верный запрос'}


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.bind((server_address, server_port))  # связываем сокет с портом, где он будет ожидать сообщения
    sock.listen(1)  # указываем сколько может сокет принимать соединений
    print('Готов к приему клиентов! \n')

    while True:
        client, address = sock.accept()  # начинаем принимать соединения
        print('соединение:', address)  # выводим информацию о подключении
        data = client.recv(1024)  # принимаем данные от клиента, по 1024 байт
        # Раскодирование байтстроки в строку, используя кодировку utf-8
        # Преобразование строки JSON в объекты Python
        client_message = json.loads(data.decode("utf-8"))
        print(f'Принято сообщение от клиента: {client_message}')
        answer = check_correct_presence_and_response(client_message)
        print(f"Приветствуем пользователя {client_message.get('user').get('account_name')}!")
        print('Отправка ответа клиенту:', answer)

        # Преобразование объекта Python в строку JSON
        # Кодируем строку в байты, используя кодировку utf-8
        client.send(json.dumps(answer).encode('utf-8'))
    client.close()  # закрываем соединение


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == '-p' and i + 1 < len(sys.argv):
                server_port = sys.argv[i + 1]
            if sys.argv[i] == '-a' and i + 1 < len(sys.argv):
                server_address = sys.argv[i + 1]
    start_server()
