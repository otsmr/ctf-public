import socket
import time
import random
from secret import *
from utils import *
from _thread import *

from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util import Padding

HOST = "127.0.0.1"
PORT = 1337

rng = random.SystemRandom()

def threaded_bob():

    print("[BOB] connect to alice")
    
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        b = rng.randint(1, prime-1)
        B = pow(generator, b, prime)

        s.send(b"B=" + bytes(str(B), 'utf-8') + b"\n")

        A = readuntil(s, b"\n")
        
        A = int(A[2:])

        K = pow(A, b, prime)

        K_hash = SHA256.new(int_to_bytes(K)).digest()

        aes = AES.new(K_hash, AES.MODE_ECB)

        # Authenticate with random_password
        # To make sure that the attacker actually is in the middle :^)

        for _ in range(3):

            # send data to the server
            current_psw = get_current_psw()
            enc = aes.encrypt(Padding.pad(current_psw, 16))
            s.send(enc.hex().encode() + b"\n")

            # get data from the server
            psw_enc = readuntil(s, b'\n').decode()
            psw_enc = bytes.fromhex(psw_enc.split(' ')[-1])
            psw = Padding.unpad(aes.decrypt(psw_enc), 16)

            if get_current_psw() != psw:
                print("[BOB] Message from Alice: ", psw)
                break

        # get the flag
        enc = bytes.fromhex(readuntil(s, b'\n').decode().split(' ')[-1])
        flag = str(Padding.unpad(aes.decrypt(enc), 16), 'utf-8')
        
        print("[BOB] Flag from Alice", flag)

        s.close()

    except Exception as e:
        print('[BOB] Error Message: ', e)

while True:

    start_new_thread(threaded_bob, ())
    time.sleep(10)