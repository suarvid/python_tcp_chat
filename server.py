import threading
import socket

host = "127.0.0.1"
port = 55557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# this is shiet, combine into User
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat.".encode())
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"new connection with address {str(address)}")

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}.")
        broadcast(f"{nickname} joined the chat.\n".encode())
        client.send("Connected to the server.\n".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()
