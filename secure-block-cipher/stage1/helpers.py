
def asciiToBinary(ascii):
    return ''.join('{:08b}'.format(ord(c)) for c in ascii)

def binaryToHex(binary):
    return hex(int(binary, 2))[2:].upper()


def messageToBlocks(message, blockSize):
    blocks = []

    for i in range(int((len(message)/blockSize)) + 1):
        block = message[(blockSize*i):(blockSize*i+blockSize)]

        if len(block) < blockSize:
            block += "0"*(blockSize-len(block)) # Padding

        blocks.append(block)

    return blocks

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