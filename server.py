import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.users_list = {}

    def threaded_client(self, conn, ip, port):

        # Pergunta ao cliente qual será seu nome cadastrado
        conn.send('Digite seu nome de usuario: '.encode())

        # Recebe o nome do usuário e checa se já existe um cliente com o mesmo nome
        username = conn.recv(1024).decode()

        while username in self.users_list:
            # Pede para o cliente um novo nome enquanto o nome escolhido estiver presente na lista
            conn.send('Nome de usuario ja existente, digite outro: '.encode())
            username = conn.recv(1024).decode()

        # Adiciona cliente à lista
        self.users_list[username] = (ip, port)

        # Envia menu de opções para o cliente
        print(self.users_list)
        conn.send('Escolha uma opção\n 1 - Ver usuários cadastrados\n 2 - Sair'.encode())
        while True:
            try:
                # Processamento da resposta
                msg = conn.recv(1024).decode()
                print('Usuário ' + username + ' escolheu a opção ' + msg)
                if msg == '1':
                    answ = 'Lista de Usuários: \n'
                    for username in self.users_list:
                        answ += '\t Username: ' + username + \
                                '\n\t IP: ' + str(self.users_list[username][0]) + \
                                '\n\t Port: ' + str(self.users_list[username][1]) + \
                                '\n\n'
                elif msg == '2':
                    self.remove_user(username)
                    conn.send('000'.encode())
                    conn.close()
                    break
                else:
                    answ = 'Opção Inválida\n'
                answ += 'Escolha uma opção\n 1 - Ver usuários cadastrados\n 2 - Sair'
                conn.send(answ.encode())
            except:
                self.remove_user(username)
                conn.close()
                break
        print('Conexao encerrada com o cliente ' + username)
        print(self.users_list)

    def remove_user(self, username):
        for l_username in self.users_list:
            if l_username == username:
                del self.users_list[username]
                break

if __name__ == '__main__':
    server = Server('localhost', 5000)

    while True:
        print("Esperando conexao...")
        conn, (ip, port) = server.sock.accept()
        print('GOT CONNECTION FROM:', (ip, port))
        thread = threading.Thread(target=server.threaded_client, args=(conn, ip, port))
        thread.start()

