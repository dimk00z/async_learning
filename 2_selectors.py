import socket
import selectors
from pprint import pprint

selector = selectors.DefaultSelector()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5001))
    server_socket.listen()

    selector.register(fileobj=server_socket,
                      events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'Connection from {addr}')
    selector.register(fileobj=client_socket,
                      events=selectors.EVENT_READ,
                      data=send_message)
    # to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = 'Hello world\n'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()
        # to_monitor.remove(client_socket)


def event_loop():
    while True:
        events = selector.select()
        for key, _ in events:
            callable = key.data
            callable(key.fileobj)


if __name__ == "__main__":
    # to_monitor.append(server_socket)
    server()
    event_loop()
