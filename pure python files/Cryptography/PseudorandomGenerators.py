# coding:utf-8
'''
Created on 20211231

@author: Yingjie Zhang
One Time Pad with bits
Linear Congruential Generator
'''
from random import randrange
import matplotlib.pyplot as plt
from random import seed

def oneTimePad():
    message = "01011101000101110101001"
    secret_key = ''.join([str(randrange(2)) for _ in range(len(message))])
    ciphertext = ''.join([str((int(m)+int(s))%2) for m, s in zip(message,secret_key)])
    print(f"message:\n\t{message}")
    print(f"secret_key:\n\t{secret_key}")
    print(f"ciphertext:\n\t{ciphertext}")

def LCG(x0,a,c,m)->int:
    return (x0*a+c)%m
    
def testLCG():
    a = 1664525
    c = 1013904223
    m = 2**32
    x0 = 433
    l = []
    xn = x0
    for _ in range(100000):
        xn = LCG(xn, a, c, m)
        l.append(xn)
    plt.clf()
    plt.figure(figsize=(16,7))
    plt.hist(l,bins=50)
    plt.show()

# testLCG()

def PRNG(s:int,l:int)->list:
    seed(s)
    prng = []
    while len(prng)< l:
        prng.append(randrange(2))
    return ''.join([str(n) for n in prng])

def testPRNG():
    s = 1234
    # Alice's end
    prng_alice = PRNG(s, 10)
    # Bob's end
    prng_bob = PRNG(s, 10)
    print(prng_alice)
    print(prng_bob)
# testPRNG()   

'''
#-------------------------------------------
# In MacOs and ubuntu 
# Calling the urandom function
import subprocess
command = "head -c 10 /dev/urandom"
process = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
output,error = process.communicate()
print(f"Random bytes:\n\t{output}")

# transform to integer bytes
int_bytes = [b for b in output]
print(f"Random bytes:\n\t{outout}\nConverted integers:\n\t{int_bytes}")

# transform to integer
int.from_bytes(output,"big")
#-------------------------------------------
'''
# using secrets to access the system random
import secrets
r = secrets.SystemRandom()
r.seed(23212)
print(bin(r.getrandbits(8))[2:])

    