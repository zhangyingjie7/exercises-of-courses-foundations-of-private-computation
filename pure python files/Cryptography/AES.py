# coding:utf-8
'''
Created on 20220104

@author: Yingjie Zhang
'''

from Cryptography.crypto import bytes_to_bin, bytes_to_hex

message = b"Cryptography is a complex subject after all..." # bytes字符串的组成形式，必须是十六进制数，或者ASCII字符：
bin_repr = bytes_to_bin(message, "")
hex_repr = bytes_to_hex(message, "")

print(f"message:\n\t{message}")
print(f"(bin):\n\t{bin_repr}")
print(f"(hex):\n\t{hex_repr}")
print(f"message is {len(message)} bytes or {len(bin_repr)} bits")

# def PKCS7(m: bytes, block_size_bytes = 16):
#     n_bytes = block_size_bytes - len(m)%block_size_bytes
#     pad = bytes([n_bytes for _ in range(n_bytes)])
#     return m+pad
# padded_message = PKCS7(message)
# print(padded_message)
print('-----------------------------------------')
from cryptography.hazmat.primitives import padding
block_size_bits = 128
padder = padding.PKCS7(block_size_bits).padder()
padded_message = padder.update(message)+padder.finalize()
print(f"message:\n\t{message}")
print(f"\npadded_data:\n\t{padded_message}\n")
print(f"bytes per block: {int(block_size_bits/8)}")
print(f"bits per block: {block_size_bits}")
print(f"message length: {len(message)}")
print(f"padded_message length: {len(padded_message)}")
print('-----------------------------------------')
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
import os

secret_key = os.urandom(32)
cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()
ctx = encryptor.update(padded_message)+encryptor.finalize()
plx = decryptor.update(ctx) + decryptor.finalize()

print(f"ciphertext:\n\t{ctx}")
print(f"plaintext:\n\t{plx}")
print('-----------------------------------------')

secret_key =os.urandom(32)
iv = os.urandom(16)
cipher = Cipher(algorithms.AES(secret_key),modes.CBC(iv),backend=default_backend())
block_size=16
for message_len in range(10):
    m = str.encode("a"*message_len)
    padder = padding.PKCS7(8*block_size).padder()
    m_padded = padder.update(m)+padder.finalize()
    encryptor = cipher.encryptor()
    ctx = encryptor.update(m_padded) + encryptor.finalize()
    print(f"message_len={message_len},padded_m_len={len(m_padded)},ctx_len={len(ctx)}")


