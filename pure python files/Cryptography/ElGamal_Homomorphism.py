# coding:utf-8
'''
Created on 20220111

@author: Yingjie Zhang
'''
from random import randrange, seed
from Cryptography.ElGamal import ElGamal

E = ElGamal()
size_bits = 64
pk, sk = E.ElGamalKeyGenerator(size_bits)
(p, g, A) = pk
(p, g, a) = sk

m1, m2 = randrange(p), randrange(p)
print("ElGamal parameters:\n-Public:\n\tp="+str(p)+"\n\tg="+str(g)+"\n\tA="+str(A))
print("\n-Private:\n\ta="+str(a)+"\n")
print("Plaintext messages:\nm1="+str(m1)+"\nm2="+str(m2)+"\n")

c1 = E.ElGamalEncrypt(m1, pk)
c2 = E.ElGamalEncrypt(m2, pk)

# plaintext multiplicatoin
plaint_mult = m1 * m2 % p

# cipher multiplication
cipher_mult = (c1[0]*c2[0]%p, c1[1]*c2[1]%p)
dec_cipher_mult = E.ElGamalDecrypt(cipher_mult, sk)

assert plaint_mult == dec_cipher_mult, "something went wrong"
print("ciphertext 1:",c1,"\nciphertext 2:",c2)
print("Product of m1 and m2 in ciphertext:",cipher_mult)
print("Decrypting the product of ciphertext:",dec_cipher_mult)
print("Product of the plaintexts:",plaint_mult)



