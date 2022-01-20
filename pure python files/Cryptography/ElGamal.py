# coding:utf-8
'''
Created on 20220109

@author: Yingjie Zhang
'''

from Cryptography.crypto import GeneratePrimeGeneratorPair,InverseFermat
from random import randrange

class ElGamal():
    '''
    Implementation of ElGamal Cryptosystem 
    '''
    def __init__(self):
        pass
    
    def ElGamalKeyGenerator(self, size_bits = 16):
        p, g = GeneratePrimeGeneratorPair(size_bits)
        a = randrange(p)
        A = pow(g, a, p)
        pk = (p, g, A)
        sk = (p, g, a)
        return pk, sk
    
    def ElGamalEncrypt(self, m, PublicKey):
        (p, g, A) = PublicKey
        k = randrange(p)
        c1 = pow(g, k, p)
        c2 = m * pow(A, k, p) % p
        return (c1, c2)
    
    def ElGamalDecrypt(self, c, SecretKey):
        (c1, c2) = c
        (p, g, a) = SecretKey
        m = c2 * InverseFermat(pow(c1, a, p), p) % p
        return m
    
    def ElGamalBruteForceAttack(self):
        (p, g, A), (p, g, a) = self.ElGamalKeyGenerator(16)
        print("p:", p)
        print("g:", g)
        print("Secret key a:", a)
        print("Public key A:", A)
        a_ = randrange(p)
        while A!= pow(g, a_, p):
            a_ = randrange(p)
        print("The secret key a:", a)
        print("The cracked secret key a_:",a_)
        
    def ElGamalKnownCiphertextAttack(self):
        size_bits = 256
        pk, sk = self.ElGamalKeyGenerator(size_bits)
        (p, g, A) = pk
        (p, g, a) = sk
        m = b"Private msg: Charlie->Alice"
        print("message:", m)
        assert 8*len(m) <= size_bits,"Message too large to encrypt in one block"
        
        m_int = int.from_bytes(m, "big")
        print("message in integer form:", m_int)
        
        # Charlie encrypts message
        (c1, c2) = self.ElGamalEncrypt(m_int, pk)
        c = (c1, c2)
        print("ciphertext:", c)
        
        # Bob intercepts message from Charlie to Alice so he knows c1 and c2 but cannot ask Alice to decrypt this
        # However he can compute $c^{\\prime}$
        m_p = randrange(p)
        k_p = randrange(p)
        c1_p = c1 * pow(g, k_p, p)%p
        c2_p = c2 * m_p * pow(A, k_p, p)%p
        c_p = (c1_p, c2_p)
        m_pp = self.ElGamalDecrypt(c_p, sk)
        print("m_pp", m_pp)
        m_int_recovered = m_pp * InverseFermat(m_p, p)%p
        m_recovered = m_int_recovered.to_bytes(len(m), "big")
        print("message:\n\t",m)
        print("message recovered:\n\t",m_recovered)
          
    
# E = ElGamal()
# pk, sk = E.ElGamalKeyGenerator(16)
# m = randrange(1,pk[0]-1)
# print("m:", m)
# c = E.ElGamalEncrypt(m, pk)
# print("c:", c)
# m1 = E.ElGamalDecrypt(c, sk)
# print("m1:", m1)
# print('--------------------------')
# E.ElGamalBruteForceAttack()
# print('--------------------------')
# E.ElGamalKnownCiphertextAttack()

