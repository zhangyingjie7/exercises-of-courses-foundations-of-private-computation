# coding:utf-8
'''
Created on 20220104

@author: Yingjie Zhang
'''
from random import randrange
bits = '0b'+''.join([str(randrange(2)) for _ in range(10)])
print("Random bits:",bits)
print("Int bits:",int(bits,2))
a = [int(k)*2**(len(bits[2:])-i-1) for i,k in enumerate(bits[2:])]
print(a)
print(sum(a))

# what is the largest number we can represent in n bits
n = 8
print(f"max integer (base 10) value for {n} bits is {2**n-1}")

bytes_int = [randrange(256) for _ in range(10)]
print(f"bytes_int\n\t{bytes_int}")
bytes_bin=[bin(x) for x in bytes_int]
print(f"bytes_bin\n\t{bytes_bin}")

n_bytes = 2
x = randrange(2**(8*n_bytes))
print(f"x in binary (base 2):\n\t{bin(x)}")
print(f"x in octal (base 8):\n\t{oct(x)}")
print(f"x in decimal (base 10):\n\t{x}")
print(f"x in hexadecimal (base 16):\n\t{hex(x)}")
print('-----------------------------------------------------------')

for i in range(128):
    b = i.to_bytes(1,byteorder='big')
    print(f"int = {i}, hex = {hex(i)}, bytes = {b}, decoded = {b.decode(encoding='UTF-8')}")
print()

x = int('e2999e',16)
x_b = x.to_bytes(4,byteorder='big')
dec_char = x_b.decode(encoding="UTF-8")
print(f"int = {x}")
print(f"bytes = {x_b}")
print(f"decoded = {dec_char}")

print('-----------------------------------------------------------')
# Turn a message from ascii letters into bytes
from crypto import bytes_to_bin, bytes_to_hex
message = b"simple message"
bin_repr = bytes_to_bin(message,pre="")
hex_repr = bytes_to_hex(message,pre="")
print(f"message:\n\t{str(message)}\n")
print(f"message in binary:\n\t{str(bin_repr)}\n")
print(f"message in hexadecimal:\n\t{str(hex_repr)}\n")