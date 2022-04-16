import socket
import random
from utils import *
from secret import *
from _thread import *

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import Padding

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

rng = random.SystemRandom()

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)

def threaded_client(conn):

    try:

        a = rng.randint(1, prime-1)
        A = pow(generator, a, prime)

        B = readuntil(conn, b'\n')

        B = int(B[2:])

        conn.send(b"A=" + bytes(str(A), 'utf-8') + b"\n")

        K = pow(B, a, prime)

        K_hash = SHA256.new(int_to_bytes(K)).digest()

        aes = AES.new(K_hash, AES.MODE_ECB)

        # Authenticate the client
        # To make sure that the attacker actually is in the middle :^)

        send_flag = False

        for _ in range(3):

            # get data from the server
            psw_enc = readuntil(conn, b'\n').decode()
            psw_enc = bytes.fromhex(psw_enc.split(' ')[-1])
            psw = Padding.unpad(aes.decrypt(psw_enc), 16)

            current_psw = get_current_psw()

            # send data to the server
            send_psw = get_current_psw()

            if  current_psw != psw:
                # this is not bob!
                enc = aes.encrypt(Padding.pad("Connection corrupted".encode(), 16))
                conn.send(enc.hex().encode() + b"\n")
                send_flag = False
                break
            else:
                enc = aes.encrypt(Padding.pad(send_psw, 16))
                conn.send(enc.hex().encode() + b"\n")

                # send the flag
                send_flag = True


        data = b"you are not the real bob!"

        if send_flag:
            data = flag.encode()
            

        print("[ALICE] send flag", data)
        enc = aes.encrypt(Padding.pad(data, 16))
        conn.send(enc.hex().encode() + b"\n")

        conn.close()

    except Exception as e:
        print('[ALICE] Error Message: ', e)


while True:

    conn, addr = s.accept()

    print('[ALICE] connected to: ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(threaded_client,(conn,))