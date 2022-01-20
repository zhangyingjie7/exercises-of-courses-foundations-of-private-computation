# coding:utf-8
'''
Created on 20220105

@author: Yingjie Zhang
'''
from Cryptography.crypto import RandomPrime,xgcd,InverseMod
from random import randrange

class RSA():
    
    def __init__(self):
        pass
    
    def RSAKeyGenerator(self,size_bits =16):
        '''
        RSA key generation. Generates public and private keys in RSA protocol.
        Input:
            size_bits: size in bits of the field
        Output:
            PublicKey: (N, e)
            PrivateKey: (N, d)
        '''
        p = RandomPrime(size_bits, m=40)
        q = RandomPrime(size_bits, m=40)
        while p==q:
            p = RandomPrime(size_bits, m=40)
        N = p*q
        phi = (p-1)*(q-1)
        # find e
        while True:
            e = randrange(2, phi-1)
            g, _, _ = xgcd(e, phi)
            if g==1:
                d = InverseMod(e, phi)
                break
        
        return (N,e),(N,d)
    
    def RSAEncrypt(self, m, PublicKey):
        '''
        Encrypts a message m using the RSA public key
        Input:
            m: message (An integer message)
        Returns:
            c: Encrypted message
        '''
        N, e = PublicKey[0], PublicKey[1]
        return pow(m, e, N)
    
    def RSADecrypt(self, c, SecretKey):
        '''
        Decrcypts the ciphertext c using the private key
        Input:
            c: Encrypted message
            SecretKey: A tuple (N, d)
        Returns:
            m: Decrypted message
        '''
        N, d = SecretKey[0], SecretKey[1]
        return pow(c, d, N)

def testRSA1():       
    rsa = RSA()
    size_bits = 16
    pk, sk = rsa.RSAKeyGenerator(size_bits)
    
    m = randrange(0, pk[0]-1)
    print("m:",str(m))
    c = rsa.RSAEncrypt(m, pk)
    print("c:",str(c))
    m1 = rsa.RSADecrypt(c, sk)
    print("decrypted m:",str(m1))

def testRSA2():
    rsa = RSA()
    size_bits = 128
    pk, sk = rsa.RSAKeyGenerator(size_bits)
    m = b"A short message"
    print("Message length in bytes", len(m))
    assert 8*len(m)<size_bits, "Message too large to encrypt in one block"
    m_int = int.from_bytes(m, "big")
    print("message in integer form", m_int)
    c_int = rsa.RSAEncrypt(m_int, pk)
    print("ciphertext in integer form", c_int)
    print()
    m_int_recovered = rsa.RSADecrypt(c_int, sk)
    print("message decrypted in integer form", m_int_recovered)
    assert m_int==m_int_recovered
    m_recovered = m_int_recovered.to_bytes(len(m), 'big')
    print("message decrypted:\n\t",m_recovered)
# testRSA2()   

# Factor N: find p and q
def PollardRho(N):
    # no prime divisor for 1
    if (N == 1):
        return N 
    
    # even number means one of the divisors is 2
    if (N % 2 == 0):
        return 2
    
    # we will pick from the range [2, N)
    x = randrange(2, N)
    y = x
    
    # the constant in f(x).
    # Algorithm can be re-run with a different if it throws failure for a composite.
    c = randrange(0, 2)
    
    # Initialize candidate divisor (or result)
    d = 1
    while (d == 1):
        x = (pow(x, 2, N) + c + N)%N
        y = (pow(y, 2, N) + c + N)%N
        y = (pow(y, 2, N) + c + N)%N
        d, _, _ = xgcd(abs(x - y), N)
        if (d == N):
            return PollardRho(N)
    return d
    
def testPollardRho():
    rsa = RSA()
    size_bits = 16
    N = rsa.RSAKeyGenerator(size_bits)[0][0]
    print(N)
    p2 = PollardRho(N)
    q2 = N//p2
    print(p2,q2)
    print(N,p2*q2)
    
testPollardRho()   