import socket
import threading
import os


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.username = ""

    def send(self, msg):
        self.sock.send(msg.encode())

    def receive(self):
        return self.sock.recv(1024).decode()

    def list_songs(self, username):
        song_folder = "./" + username

        if not os.path.exists(song_folder):
            os.makedirs(song_folder)

        song_list = os.listdir(song_folder)

        if len(song_list) == 0:
            song_list = {"pasta_vazia"}

        return song_list

    def list_to_str(self, list):
        answ = " ".join(str(s) for s in list)
        return answ


if __name__ == "__main__":
    client = Client("localhost", 5000)
    while True:
        msg = client.receive().split(" ")
        if msg[0] == "000":
            print("Conexão encerrada")
            break
        elif msg[0] == "request_song_list":
            song_list = client.list_songs(msg[1])
            msg = client.list_to_str(song_list)
            client.send(msg)
        else:
            print(" ".join(msg))
            msg = input()
            client.send(msg)


