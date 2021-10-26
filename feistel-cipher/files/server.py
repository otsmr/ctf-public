import socket
from _thread import *
from helpers import readuntil, asciiToBinary, hexToBinary, binaryToAscii
from secret import flag
from cipher import decrypt, BLOCKSIZE

host = "0.0.0.0"
port = 1337
flag = asciiToBinary(flag)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

print("Listening")
s.listen(5)

def threaded_client(conn):

    conn.send(
b"""
--- Secure safe ----
Decrypt your secret messages
without having to remember the key.

Enter ciphertext:
""")

    cipher = readuntil(conn, b'\n').decode()

    try:
        
        l = int(BLOCKSIZE/8)*2
        cipher = hexToBinary((cipher + ("00"*l))[:l])

    except:
        conn.send(b"No valid ciphertext")
        conn.close()
        return

    plaintext = decrypt(cipher, flag)
    conn.send(b"Decrypted message: " + binaryToAscii(plaintext).encode() + b"\n")
    conn.close()

while True:

    conn, addr = s.accept()
    print('connected to: ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client,(conn,))