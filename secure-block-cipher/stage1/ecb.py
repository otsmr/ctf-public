import random
from secret import flag
from helpers import asciiToBinary, binaryToHex, messageToBlocks
from cipher import encrypt

# Metadata
blockSize = 40

# Generate a random key
key = "".join([str(random.randint(0, 1)) for _ in range(blockSize*2)])

# Convert message to binary representation 
message = asciiToBinary(flag)

# Electronic Code Book Mode
messageBlocks = messageToBlocks(message, blockSize)
chiphers = [encrypt(m, key) for m in messageBlocks]

chipher = binaryToHex("".join(chiphers))
print("Ciphertext:", chipher)