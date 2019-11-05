# --IMPORT
import socket

# --VARIABILI
boolD = True


# --FUNZIONI
def dataToBytes(data):
    bytes = bytearray()
    for d in data:
        bytes += (bytearray(d.encode()))
        if data.index != len(data) - 1:
            bytes.append(0)
    return bytes


# --MAIN
if __name__ == "__main__":
    if boolD:
        print("Start")

    host = socket.gethostname()
    port = 2000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    logpack = bytearray()
    logpack.append(11)
    bite = dataToBytes(["Francesco", "Ciao"])
    logpack += (len(bite).to_bytes(2, byteorder="big"))
    logpack += bite

    sock.send(logpack)
    while True:
        sock.listen(1)
        r = sock.recv(1024)
        print(r)

    # sock.close()

    # if boolD:
    #   print("End")
