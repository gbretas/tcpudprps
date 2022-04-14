import socket
import threading
import logging
import signal
import sys
import random

#global var
ip = "127.0.0.1"
port_udp = "1740"

database = [
        ['mafe', '123'],
        ['murta', '123'],
        ['yan', '123'],
        ['gustavo', '123'] 
    ]

sessions = []
sessions_username = []
placar = []


def check_rps(one, second):
    if one == "R" and second == "S":
        return 1
    elif one == "R" and second == "P":
        return 2
    elif one == "S" and second == "R":
        return 2
    elif one == "S" and second == "P":
        return 1
    elif one == "P" and second == "R":
        return 1
    elif one == "P" and second == "S":
        return 2
    elif one == second:
        return 0
    else:
        return -1

def udp_auth():

    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind((ip,int(port_udp)))

    while True:
        x = server_udp.recvfrom(1024)
        ip_user = str(str(x[1][0])+":"+str(x[1][1]))
        data = x[0].decode()

        if ip_user not in sessions:
            if 'user:' in data:
                splitted =  data.split('user:')[1]
                username = splitted.split(':')[0]
                password = splitted.split(':')[1]
                if [username, password] in database:
                    sessions.append(ip_user)
                    sessions_username.append(username)
                    print(username + ' logged in from UDP via '+ ip_user)
                else:
                    print(username + ' error in login')
            else:
                print("Usuário sem permissão para acessar o sistema")
        else:
            user = sessions_username[sessions.index(ip_user)]
            print(ip_user + " ("+user+") : " + data)

def on_new_client(client,addr):
        data = client.recv(1024)

        ip_conn = str(addr[0]+":"+str(addr[1]))

        if data.decode() in sessions_username or ip_conn in sessions:
            index = sessions_username.index(data.decode())
            sessions[index] = str(addr[0])+":"+str(addr[1])
            print ("Cliente: " + data.decode() + " conectado TCP pelo ip: " + str(addr[0])+":"+str(addr[1]))
            client.send(str.encode("Bem vindo ao jogo Rock Paper Scissors\nPara jogar digite R para Pedra, P para papel e S para tesoura\nDigite sua jogada: "))

            while True:
                data = client.recv(1024)
                if not data or data.decode() == "sair":
                    print("Cliente: " + sessions_username[index] + " desconectado pelo TCP usando o ip: " + str(addr[0])+":"+str(addr[1]))
                    client.send(str.encode("Obrigado por jogar"))
                    client.close()
                    break
                elif data.decode() == "placar":
                    placar_show = ""
                    for i in range(len(placar)):
                        placar_show += sessions_username[i]+" - "+str(placar[i])+"\n"
                    client.send(str.encode("Placar: \n" + str(placar_show) +"\nDigite sua nova jogada, ou digite 'sair' para sair:"))

                else:
                    data_decoded = (data.decode()).upper()
                    robot_random = str(random.choice(['R','P','S']))
                    if robot_random == "R":
                        robot_random_name = "Pedra"
                    elif robot_random == "P":
                        robot_random_name = "Papel"
                    elif robot_random == "S":
                        robot_random_name = "Tesoura"

                    flag = 1
                    if data_decoded == "R":
                        retorno = "Você jogou Pedra e o computador jogou " + robot_random_name + "\n"
                    elif data_decoded == "P":
                        retorno = "Você jogou Papel e o computador jogou " + robot_random_name + "\n"
                    elif data_decoded == "S":
                        retorno = "Você jogou Tesoura e o computador jogou " + robot_random_name + "\n"
                    else:
                        flag = 0
                        retorno = "Jogada inválida\n"
                    
                    if flag == 1:
                        check = check_rps(data_decoded, robot_random)

                        if data_decoded == "R":
                            data_decoded_name = "Pedra"
                        elif data_decoded == "P":
                            data_decoded_name = "Papel"
                        elif data_decoded == "S":
                            data_decoded_name = "Tesoura"

                        if check == 0:
                            retorno += "O jogo terminou empatado"
                            print("Cliente: " + sessions_username[index] + " empatou jogada com o computador" + " ("+robot_random_name+")")
                        elif check == 1:
                            retorno += "Você ganhou"
                            try:
                                placar[index] += 1
                            except IndexError:
                                placar.insert(index, 1)
                            print ("Cliente: " + sessions_username[index]  + " ganhou com " + data_decoded_name + " contra " + robot_random_name)
                        else:
                            retorno += "Você perdeu"
                            print ("Cliente: " + sessions_username[index] + " perdeu com " + data_decoded_name + " contra " + robot_random_name)
                        
                        retorno += "\nDigite sua nova jogada, ou digite 'sair' para sair: "
                    client.send(str.encode(retorno))


        else:
            print("Cliente sem permissão para acessar o sistema")
            client.send(str.encode("Cliente sem permissão para acessar o sistema"))
            client.close()

def rock_paper_scissors():
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp.bind((ip,int(port_udp)+1))
    server_tcp.listen(5)
    while True:
        c, addr = server_tcp.accept()     # Establish connection with client.
        threading.Thread(target=on_new_client,args=(c,addr)).start()


if __name__ == "__main__":

    print("Iniciando o servidor de autenticação UDP em Threading")
    x = threading.Thread(target=udp_auth, args=())
    x.start()

    print("Iniciando o servidor do Game")
    y = threading.Thread(target=rock_paper_scissors, args=())
    y.start()
    
