#   IMPORT
import socket
import threading

#   VARIABILI
boolD = True
users = []


#   FUNZIONI
def connect(sockCli, host):
    username = ""
    log = False
    while (True):
        sock.listen(1)
        pack = sockCli.recv(1024)
        if len(pack) > 0:
            if pack[0] == 10:
                err = registrazione(pack)
                if err:
                    sockCli.send(error("Nome utente già presente"))
                else:
                    sockCli.send(OK())
            elif pack[0] == 11:
                err = login(pack, sockCli)
                if err == "Passoword non trovata" or err == "Username non trovato":
                    sockCli.send(error(err))
                else:
                    username = err
                    log = True
                    sockCli.send(OK())
            if log:
                if pack[0] == 12:
                    err = logout(username)
                elif pack[0] == 20:
                    pass
                elif pack[0] == 22:
                    err = privateMessage(pack, username)
                    if err:
                        sockCli.send(error("Messaggio non inviato"))
                    else:
                        sockCli.send(OK())
                elif pack[0] == 24:
                    pass


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


def logout(username):
    for i in range(len(users)):
        user = users[i]
        if user[0] == username:
            del users[i]


def login(pack, sockCli):
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
                users.append((username, sockCli))
                return username
            else:
                return "Passoword non trovata"
    return "Username non trovato"


def registrazione(pack):
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
    return addUser(username, password)


def addUser(username, password):
    fopen = open("../User/users.csv", "r")
    for line in fopen:
        campi = line.split(";")
        if campi[0].replace("\"", "") == username:
            fopen.close()
            return True
    fopen = open("../User/users.csv", "a")
    fopen.write("\"" + username + "\";\"" + password + "\"\n")
    fopen.close()
    return False


def privateMessage(pack, user):
    i = 3
    cc = True  # ContaCampi
    dest = ""
    text = ""
    while (i < len(pack)):
        if pack[i] == 0:
            cc = False
            i += 1
        if cc:
            dest += chr(pack[i])
        else:
            text += chr(pack[i])
        i += 1

    socket_dest = ""
    for us in users:
        if us[0] == dest:
            socket_dest = us[1]

    pack_to_send = createMexPack(23, user, text)
    socket_dest.send(pack_to_send)
    try:
        return False
    except:
        return True


def createMexPack(mode, mitt, text):
    mex = bytearray()

    mex.append(mode)
    info = dataToBytes([mitt, text])
    mex += (len(info).to_bytes(2, byteorder="big"))
    mex += (info)

    if boolD:
        print(mex)

    return mex


def dataToBytes(data):
    bytes = bytearray()
    for d in data:
        bytes += (bytearray(d.encode()))
        if data.index(d) != len(data) - 1:
            bytes.append(0)
    print(bytes)
    return bytes


#   MAIN
if __name__ == "__main__":
    if boolD:
        print("Inizio programma")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("172.16.20.143", 2000))
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
