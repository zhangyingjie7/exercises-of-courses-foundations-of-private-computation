# coding:utf-8
'''
Created on 20220104

@author: Yingjie Zhang
'''

import os
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend

secret_key = os.urandom(32)
nonce = os.urandom(16)
print(len([bin(x) for x in secret_key]))
print([bin(x) for x in secret_key])
print(nonce)
algorithm = algorithms.ChaCha20(secret_key,nonce)

chachacipher = Cipher(algorithm,mode = None,backend=default_backend())
encryptor = chachacipher.encryptor()
decryptor = chachacipher.decryptor()

message = b"A super secret message"
ctx = encryptor.update(message)
ptx = decryptor.update(ctx)
print(f"original message:\n\t{message}")
print(f"ctx:\n\t{ctx}")
print(f"recovered message:\n\t{ptx}")

print()
for message_len in range(32):
    message = str.encode("a"*message_len)
    ctx = encryptor.update(message)
    print(f"message_len: {message_len}, ciphertext_len: {len(ctx)}")