# coding:utf-8
'''
Created on 20220104

@author: Yingjie Zhang
'''

from Cryptography.crypto import binary, hexadecimal
import random

a = random.randrange(256)
b = random.randrange(256)

print(f"a: {a} (int), {hexadecimal(a,pre='')} (hex), {binary(a,pre='')} (bin)")
print(f"b: {b} (int), {hexadecimal(b,pre='')} (hex), {binary(b,pre='')} (bin)")

xored = a ^ b
print(f"xored: {xored} (int), {hexadecimal(xored,pre='')} (hex), {binary(xored,pre='')} (bin)")
print()


random.seed(10)
state = random.getstate()
print([random.randrange(256) for _ in range(10)])
random.setstate(state)
print([random.randrange(256) for _ in range(10)])
print()

def PseudoRandomBytes(state: tuple, l: int) -> (bytes,tuple):
    """
    Generates a stream of pseudorandom bytes
    Input:
        - state: a state for the python random package (random.getstate())
        - l: length of the pseudorandom stream of bytes
    Returns:
        - state: the current state of the random
        - bytestream: a bytes class of length l
    """
    random.setstate(state)
    prng = []
    while len(prng) < l:
        prng.append(hexadecimal(random.randrange(256)))
    return random.getstate(), bytes([int(x,0) for x in prng])
    
state = random.getstate()
l = 20
new_state, prng = PseudoRandomBytes(state,l) 
print(new_state)
print(prng)

print()

class Party:
    def __init__(self, state: tuple):
        self._state = state
    
    def encrypt_decrypt(self,m:bytes) -> bytes:
        new_state, random_bytes =  PseudoRandomBytes(self._state,len(m))
        self._state = new_state 
        return bytes([a ^ b for a, b in zip(m,random_bytes)])  

state = random.getstate()
alice = Party(state)
bob = Party(state)

m = b"Hi Bob. How are you doing?"
ctx = alice.encrypt_decrypt(m)
m2 = bob.encrypt_decrypt(ctx)
print(f"message:\n\t{m}\n")
print(f"ciphertext:\n\t{ctx}\n")
print(f"recovered_message:\n\t{m2}\n")