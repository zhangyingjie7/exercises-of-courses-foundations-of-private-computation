# coding:utf-8
'''
Created on 20220110

@author: Yingjie Zhang
'''

from random import randrange, seed
from Cryptography.RSA import*

size_bits = 64
seed(3)

RSA = RSA()
pk, sk = RSA.RSAKeyGenerator(size_bits)
(N,e), (N,d) = pk, sk

m1, m2 = randrange(N), randrange(N)
print("RSA parameters:\n-Public:\n\tN="+str(N)+"\n\te="+str(e))
print("\n-Private:\n\td="+str(d)+"\n")
print("Plaintext message:\nm1="+str(m1)+"\nm2="+str(m2)+"\n")
mult = m1 * m2 % N
mult2 = RSA.RSADecrypt(RSA.RSAEncrypt(m1, pk) * RSA.RSAEncrypt(m2, pk), sk)
print("plaintext multiplication:", str(mult))
print("ciphertext multiplication and decryption:", str(mult2))