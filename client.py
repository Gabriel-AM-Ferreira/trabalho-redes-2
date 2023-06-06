import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, msg):
        self.sock.send(msg.encode())
        
    def receive(self):
        return self.sock.recv(1024).decode()

if __name__ == '__main__':
    client = Client('localhost', 5000)
    while True:
        msg = client.receive()
        if msg == '000':
            print('Conexão encerrada')
            break
        print(msg)
        msg = input()
        client.send(msg)
