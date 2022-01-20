# coding:utf-8
'''
Created on 20220105

@author: Yingjie Zhang
'''

from Cryptography.crypto import LCM,RandomPrime,xgcd,InverseMod
from random import randrange

class Paillier():
    '''
    Implementation of Paillier Cryptosystem 
    '''
    def __init__(self):
        pass
    
    def _L(self, x, n):
        return (x-1)//n
    
    def PaillierKeyGenerator(self, size_bits = 16):
        '''
        This function generates public and private keys
        Input:
            size: size in bits of the field
        Output:
            PublicKey: (N, g)
            PrivateKey: (N, l, mu)
        '''
        gcd = 2
        while gcd != 1:
            p = RandomPrime(size_bits, m=40)
            q = RandomPrime(size_bits, m=40)
            while p==q:
                q = RandomPrime(size_bits, m=40)
            N = p*q
            gcd, _, _ = xgcd(N, (p-1)*(q-1))
            
        l = LCM(p-1, q-1)
        nsq = N*N
        mu = None
        while mu == None:
            g = randrange(1, nsq)
            mu = InverseMod(self._L(pow(g, l, nsq), N), N)
        pk = (N, g)
        sk = (N, l, mu)
        return pk, sk
    
    def PaillierEncrypt(self, m, PublicKey):
        '''
        Encrypts a message m using the Paillier public key
        Input:
            m: message (An integer message) (mod N)
            PublicKey: A tuple (N, g)
        Output:
            c: Encrypted message
        '''
        (N, g) = PublicKey
        gcd = 2
        while gcd != 1:
            r = randrange(1, N)
            gcd, _, _ = xgcd(r, N)
        c = pow(g, m, N*N)*pow(r, N, N*N)%(N*N)
        return c
    
    def PaillierDecrypt(self, c, SecretKey):
        '''
        Decrypts a ciphertext m using the Paillier private key
        Input:
            m: message (An integer message) (mod N)
            SecretKey: A tuple (N, l, mu)
        Output:
            m: Decrypted message
        '''
        (N, l, mu) = SecretKey
        m2 = self._L(pow(c, l, N*N),N)*mu%N
        return m2 
        
        
    

# P = Paillier()
# pk, sk = P.PaillierKeyGenerator(16)
# m = randrange(0,pk[0])
# c = P.PaillierEncrypt(m, pk)
# print("m:", m)
# print("c:", c)
# m2 = P.PaillierDecrypt(c, sk)
# print("Recovered message:", m2)

