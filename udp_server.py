import socket
import threading

# Настройки сервера
SERVER_HOST = 'localhost'
SERVER_PORT = 9090
BUFFER_SIZE = 1024

# Список клиентов
clients = []

# Создание сокета UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")


def broadcast(message, sender_address):
    """Отправка сообщения всем клиентам, кроме отправителя."""
    for client in clients:
        if client != sender_address:
            server_socket.sendto(message, client)


def handle_messages():
    """Обработка входящих сообщений."""
    while True:
        # Получение данных от клиента
        data, addr = server_socket.recvfrom(BUFFER_SIZE)

        if addr not in clients:
            clients.append(addr)
            print(f"Новый клиент подключился: {addr}")

        print(f"Сообщение от {addr}: {data.decode('utf-8')}")

        # Трансляция сообщения всем клиентам
        broadcast(data, addr)


# Запуск обработки сообщений
message_handler = threading.Thread(target=handle_messages, daemon=True)
message_handler.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nСервер остановлен.")
    server_socket.close()
