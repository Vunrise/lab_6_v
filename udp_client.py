import socket
import threading

# Настройки клиента
SERVER_HOST = 'localhost'
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# Создание сокета UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)  # Установим сокет в неблокирующий режим

print("Подключение к серверу...")
server_address = (SERVER_HOST, SERVER_PORT)

nickname = input("Введите ваш ник: ")


def send_messages():
    """Отправка сообщений на сервер."""
    try:
        while True:
            message = input()
            if message.lower() == "exit":
                print("Вы отключились от чата.")
                break
            full_message = f"{nickname}: {message}"
            client_socket.sendto(full_message.encode('utf-8'), server_address)
    finally:
        client_socket.close()


def receive_messages():
    """Получение сообщений от сервера."""
    while True:
        try:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            print(data.decode('utf-8'))
        except BlockingIOError:
            continue  # Ожидание новых сообщений
        except OSError:
            # Закрытие сокета приведёт к ошибке, выходим из цикла
            break


# Поток для получения сообщений
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Основной цикл отправки сообщений
try:
    send_messages()
finally:
    client_socket.close()
