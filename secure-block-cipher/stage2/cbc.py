import random
from secret import flag
from helpers import asciiToBinary, binaryToHex, messageToBlocks, XOR, XORString

from cipher import encrypt

# Metadata
blockSize = 40

# Generate a random key & IV
key = "".join([str(random.randint(0, 1)) for _ in range(blockSize*2)])
IV = "".join([str(random.randint(0, 1)) for _ in range(blockSize)])

# Convert message to binary representation 
message = asciiToBinary(flag)

# Cipher Block Chaining Mode
messageBlocks = messageToBlocks(message, blockSize)

chiphers = []

for m in messageBlocks:

    chain = chiphers[len(chiphers)-1] if len(chiphers) > 0 else IV

    z = XORString(m, chain)
    c = encrypt(z, key)

    chiphers.append(c)

chipher = binaryToHex("".join(chiphers))

# Print Ciphertext
print("IV:", binaryToHex(IV))
print("Ciphertext:", chipher)