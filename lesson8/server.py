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
import logging
import select
import sys
from config import ACTION, PRESENCE, TIME, RESPONSE, OK, WRONG_REQUEST, \
    ERROR, server_port, server_address, MAX_CONNECTIONS
import socket
import decorators
import logs.config.server_config_log
import argparse
import pickle

log = logging.getLogger('Server_log')
logger = decorators.Log(log)


@logger
def check_correct_presence_and_response(presence_message):
    log.info('Запуск функции проверки корректности запроса')
    if ACTION in presence_message and \
            presence_message[ACTION] == PRESENCE and \
            TIME in presence_message and \
            isinstance(presence_message[TIME], str):
        return {RESPONSE: OK}
    else:
        return {RESPONSE: WRONG_REQUEST, ERROR: 'Не верный запрос'}


@logger
def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
    sock.bind((server_address, server_port))  # связываем сокет с портом, где он будет ожидать сообщения
    sock.settimeout(0.5)

    clients = []  # список клиентов
    messages = []  # очередь сообщений

    sock.listen(MAX_CONNECTIONS)  # указываем сколько может сокет принимать соединений
    log.info('Готов к приему клиентов! \n')

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, address = sock.accept()  # начинаем принимать соединения
        except OSError:
            pass
        else:
            log.info('соединение:', address)  # выводим информацию о подключении
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    data_bytes = client_with_message.recv(1024)  # принимаем данные от клиента, по 1024 байт
                    client_message = pickle.loads(data_bytes)  # Преобразование строки JSON в объекты Python
                    log.info(f'Принято сообщение от клиента: {client_message}')
                    answer = check_correct_presence_and_response(client_message)
                    messages.append(answer)
                    log.info(f"Приветствуем пользователя {client_message.get('user').get('account_name')}!")
                except:
                    log.info(f"Клиент {client_message.get('user').get('account_name')} отключился от сервера.")
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            for waiting_client in send_data_lst:
                for answer in messages:
                    try:
                        log.info('Отправка ответа клиенту:', answer)
                        data_bytes = pickle.dumps(answer)  # Преобразование объекта Python в строку JSON
                        waiting_client.send(data_bytes)
                    except:
                        log.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        clients.remove(waiting_client)
            # после отправки всех сообщений очищаем список сообщений
            messages = []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='Port server', default=server_port)
    parser.add_argument('-a', '--address', type=str, help='Address server', default=server_address)
    args = parser.parse_args()

    server_port = args.port
    server_address = args.address

    # Показывать лог в консоль при запуске сервера напрямую
    server_stream_handler = logging.StreamHandler(sys.stdout)
    server_stream_handler.setLevel(logging.INFO)
    server_stream_handler.setFormatter(logs.config.server_config_log.log_format)
    log.addHandler(server_stream_handler)

    start_server()
