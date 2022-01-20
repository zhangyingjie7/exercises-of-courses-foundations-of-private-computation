# coding:utf-8
'''
Created on 20220110

@author: Yingjie Zhang
'''

from random import randrange, seed
from Cryptography.Paillier import Paillier


P = Paillier()
size_bits = 64
pk, sk = P.PaillierKeyGenerator(size_bits)
(N, g), (N, l, mu) = pk, sk

m1, m2 = randrange(2, N*N), randrange(2, N*N)
print("Paillier parameters:\n-Public:\n\tN="+str(N)+"\n\tg="+str(g))
print("\n-Private:\n\tN="+str(N)+"\n\tlambda="+str(l)+"\n\tmu="+str(mu))
print("Plaintext messages:\nm1="+str(m1)+"\nm2="+str(m2)+"\n")
print("Sum modulo N of plaintext:"+str((m1+m2)%N))
prod_ciphertext = P.PaillierEncrypt(m1, pk) * P.PaillierEncrypt(m2, pk) % (N**2)
decrypted_prod = P.PaillierDecrypt(prod_ciphertext, sk)
print("Decryption of the product encoded:",decrypted_prod)
assert decrypted_prod==(m1+m2)%N, "something went wrong"

prod_ciphertext2 = P.PaillierEncrypt(m1, pk) * pow(g, m2, N**2) % (N**2)
decrypted_prod2 = P.PaillierDecrypt(prod_ciphertext2, sk)
assert decrypted_prod2==(m1+m2)%N, "something went wrong"
print("Decryption of the product2 encoded:", decrypted_prod2)