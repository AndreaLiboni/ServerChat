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
                    sockCli.send(error("Nome utente gia' presente"))
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
                    if err:
                        sockCli.send(OK())
                        sockCli.close()
                        break
                    else:
                        sockCli.send(error("Utente non trovato"))
                elif pack[0] == 20:
                    err = broadcast(pack, username)
                    if err:
                        sockCli.send(error("Messaggio non inviato"))
                    else:
                        sockCli.send(OK())
                elif pack[0] == 22:
                    err = privateMessage(pack, username)
                    if err:
                        sockCli.send(error("Messaggio non inviato"))
                    else:
                        sockCli.send(OK())
                elif pack[0] == 24:
                    err = multicast(pack, username)
                    if err:
                        sockCli.send(error("Messaggio non inviato"))
                    else:
                        sockCli.send(OK())
                elif pack[0] == 42:
                    err = list()
                    if err:
                        sockCli.send(error("ERRORE"))
                    else:
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
                for i in len(users):
                    if username == users[i][0]:
                        return "Utente gia' online"
                users.append((username, sockCli))
                return username
            else:
                return "Passoword non trovata"
    return "Username non trovato"


def logout(username):
    for i in range(len(users)):
        user = users[i]
        if user[0] == username:
            # user[1].close()
            del users[i]
            return True
    return False


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


def broadcast(pack, user):
    text = ""
    i = 3
    while i < len(pack):
        text += chr(pack[i])
        i += 1

    dests = []
    for us in users:
        if us != user[0]:
            dests.append(us[0])

    try:
        sender(21, dests, text, user)
        return False
    except:
        return True


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

    try:
        sender(23, [dest], text, user)
        return False
    except:
        return True


def multicast(pack, user):
    vett = []
    i = 3
    dest = ""
    while (i < len(pack)):
        if pack[i] == 0:
            vett.append(dest)
            dest = ""
        dest += chr(pack[i])
        i += 1
    destinatari = []
    text = ""
    for i in range(len(vett)):
        if i + 1 >= len(vett):
            text = vett[i]
        else:
            destinatari.append(vett[i])
    print(text)
    print(destinatari)
    sender(25, destinatari, text, user)


def sender(mode, dest, text, mitt):
    sock_dest = []
    for d in dest:
        for us in users:
            if us[0] == d:
                sock_dest.append(us[1])

    pack = createMexPack(mode, mitt, text)
    for sd in sock_dest:
        sd.send(pack)


def createMexPack(mode, mitt, text):
    mex = bytearray()

    mex.append(mode)
    info = dataToBytes([mitt, text])
    mex += (len(info).to_bytes(2, byteorder="big"))
    mex += (info)

    return mex


def list():
    online_users = []
    for us in users:
        online_users.append(us[0])

    online_users = dataToBytes(online_users)

    pack = bytearray()
    pack.append(43)

    pack += len(online_users)
    pack += online_users

    try:
        sockCli.send(pack)
        return False
    except:
        return True


def dataToBytes(data):
    bytes = bytearray()
    for d in data:
        bytes += (bytearray(d.encode()))
        if data.index(d) != len(data) - 1:
            bytes.append(0)
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
        # for i in range(len(users)):
        #     print(users[i])
