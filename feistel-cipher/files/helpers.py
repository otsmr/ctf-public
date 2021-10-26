def readuntil(sock, char):
    ret = b''
    while True:
        c = sock.recv(1)
        if char in ret + c:
            break
        ret += c
    return ret

def asciiToBinary(ascii):
    return ''.join('{:08b}'.format(ord(c)) for c in ascii)

def binaryToAscii(binaryString):
    return "".join([chr(int(binaryString[i:i+8],2)) for i in range(0,len(binaryString),8)])

def binaryToHex(binary):
    return hex(int(binary, 2))[2:].upper()

def XOR(s1, s2):
    if s1 == s2:
        return "0"
    return "1"

def XORString(s1, s2):
    return "".join([XOR(s1[i], s2[i]) for i in range(len(s1))])

def hexToBinary(hex):
    a = "{0:020b}".format(int(hex, 16))
    while len(a) < len(hex)*4:
        a = "0"+a
    return a