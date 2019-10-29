#   IMPORT
import socket
import threading

#   VARIABILI
boolD = True
users = []

# ciao ciao sasasa prova 1 2 3

#   FUNZIONI
def connect(sockCli, host):
    while (True):
        sock.listen(4)
        pack = sockCli.recv(1024)
        if len(pack) > 0:
            if pack[0] == 10:
                err = registrazione(pack)
                if err:
                    sockCli.send(error("Nome utente già presente"))
                else:
                    sockCli.send(OK())
            elif pack[0] == 11:
                err = login(pack)
                if err:
                    sockCli.send(error("Nome utente o password non validi"))
                else:
                    sockCli.send(OK())


def OK():
    mex = bytearray()
    mex.append(0)
    mex += (0).to_bytes(2, byteorder="big")
    return mex

def error(string):
    mex = bytearray()
    mex.append(1)
    data = string.encode()
    mex += len(data).to_bytes(2, byteorder="big")
    mex += data
    return mex

def login(pack):
    i = 3
    cc = True  # ContaCampi
    username = ""
    password = ""
    while (i < len(pack)):
        if pack[i] == 0:
            cc = False
            i += 1
        if cc:
            username += chr(pack[i])
        else:
            password += chr(pack[i])
        i += 1
    fopen = open("../User/users.csv", "r")
    for line in fopen:
        campi = line.replace("\"", "").split(";")
        if campi[0] == username:
            if campi[1].rstrip("\n") == password:
                users.append(username)
                return True
            else:
                return False
    return False

def registrazione(pack):
    i = 3
    cc = True   #ContaCampi
    username = ""
    password = ""
    while (i < len(pack)):
        if pack[i] == 0:
            cc = False
            i += 1
        if cc:
            username += chr(pack[i])
        else:
            password += chr(pack[i])
        i += 1
    return addUser(username, password)


def addUser(username, password):
    fopen = open("../User/users.csv", "r")
    for line in fopen:
        campi = line.split(";")
        if campi[0].replace("\"","") == username:
            fopen.close()
            return True
    fopen = open("../User/users.csv", "a")
    fopen.write("\"" + username +"\";\"" + password + "\"\n")
    fopen.close()
    return False

#   MAIN
if __name__ == "__main__":
    if boolD:
        print("Inizio programma")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("172.16.20.6", 2000))
    print("Per collegarsi usare il seguente nome e specificare la porta 2000:" + socket.gethostname())
    sock.listen(4)
    connections = []
    conta = 0
    while True:
        sockCli, host = sock.accept()
        print("La connessione è stata stabilita con l'host: " + host[0] + ":" + str(host[1]))
        connections.append(threading.Thread(target=connect, args=(sockCli, host)))
        connections[conta].start()
        conta += 1
        for i in range(len(users)):
            print(users[i])