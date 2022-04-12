#!/usr/bin/env python
from ast import While
import socket
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



name = input("Enter your username: ")
password = input("Enter your password: ")

server_ip = "127.0.0.1"
server_port = "1781"
port_game = (int(server_port)+1)



def authenticate_udp():
    auth = 0
    try:
        server.connect((server_ip,int(server_port)))
        if auth == 0:
            a="user:"+name+":"+password
            b = a.encode()
            server.send(b)
            auth = 1
    except Exception as e:
        print(e)
        print("Server is not responding")


def game_tcp():
    try:
        server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_tcp.connect((server_ip,int(port_game)))
        # Conectado ao servidor
        data = name
        server_tcp.send(data.encode())
        data = server_tcp.recv(1024)
        print(data.decode())

        if data.decode() != "Cliente sem permissão para acessar o sistema":
            while True:
                jogada = input()
                jogada = jogada.lower()
                if jogada not in ['r','p','s', 'sair']:
                    print("Jogada inválida")
                else:
                    server_tcp.send(jogada.encode())
                    data = server_tcp.recv(1024)
                    print(data.decode())
    except Exception as e:
        #close con
        print(e)
        print("Server is not responding")
        server_tcp.close()


    # data = input("")
    

if __name__ == "__main__":
    authenticate_udp()
    game_tcp()

    #connect via tcp to game

