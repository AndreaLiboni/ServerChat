#   IMPORT
import socket

#   VARIABILI
boolD = True

#   FUNZIONI
def createMex():
    pack = bytearray()
    pack.append(11)
    data = createData()
    pack += len(data).to_bytes(2, byteorder="big")
    pack += data
    return pack

def createData():
    data = bytearray()
    data += ("Andrea".encode())
    data.append(0)
    data += ("Ciao".encode())
    return data

#   MAIN
if __name__ == "__main__":
    if boolD:
        print("Inizio programma")
        host = "LAPTOP-P1G7L1TM"
        port = 2000
    else:
        host = input("Inserire l'indirizzo IP del server:")
        port = int(input("Inserire la porta del server:"))
    mex = createMex()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(5)
    sock.send(mex)
    print("Il messaggio inviato è: " + str(mex))
    mexRic = sock.recv(1024)
    print("Il messaggio ricevuto è:" + str(mexRic))
    ####################################
    pack = bytearray()
    pack.append(22)
    ###########
    data = bytearray()
    data += ("Francesco".encode())
    data.append(0)
    data += ("Ciao mondo".encode())
    ###########
    pack += len(data).to_bytes(2, byteorder="big")
    pack += data

    sock.send(pack)
    print("Il messaggio inviato è: " + str(pack))
    mexRic = sock.recv(1024)
    print("Il messaggio ricevuto è:" + str(mexRic))
    sock.close()
    if boolD:
        print("Fine programma")