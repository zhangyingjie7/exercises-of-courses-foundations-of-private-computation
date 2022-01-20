# coding:utf-8
'''
Created on 20220111

@author: Yingjie Zhang
'''

from collections import namedtuple
import secrets
from typing import List, Tuple

import numpy as np  # type: ignore

PrivateKey = namedtuple("PrivateKey", ["lam", "mu"])
PublicKey = namedtuple("PublicKey", ["g", "n", "n_squared"])

DEFAULT_BIT_LENGTH = 3072

def xgcd(a, b):
    # Solving equation au+bv=gcd(a,b)
    # result is: (g,u,v) where g is greatest common divisor and u,v the solution of the eq above
    u0, u1, v0, v1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        v0, v1 = v1, v0 - q * v1
        u0, u1 = u1, u0 - q * u1
    return b, u0, v0

def InverseMod(a: int, m: int) -> int:
    """
    Given natural number a and m returns b = a^{-1}(mod m). The inverse modulo m of a.
    This is b*a (mod p )=1
    Input:
        a: an integer element of the field (1 < a < m)
        m: an integer
    Output:
        b: The inverse modulo m of a
    e.g.
    a = 10
    m = 7
    inv_a = InverseMod(a,m)
    print("inverse of {} in modulo {} is {}\na*inv_a = {}".format(a,m,inv_a,a*inv_a%m))
    """
    g, u, _ = xgcd(a,m)
    if g!=1:
        #print("{} has no inverse on modulo {}".format(a,m))
        return None
    return u%m



# Copy and paste your function from the Cryptography lesson or uncomment this code:
def generate_primes(n: int) -> List[int]:
    # https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Input n>=6, Returns an array of primes, 2 <= p < n """
    sieve = np.ones(n // 3 + (n % 6 == 2), dtype=np.bool)
    for i in range(1, int(n ** 0.5) // 3 + 1):
        if sieve[i]:
            k = 3 * i + 1 | 1
            sieve[k * k // 3 :: 2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3 :: 2 * k] = False
    primes = np.r_[2, 3, ((3 * np.nonzero(sieve)[0][1:] + 1) | 1)]
    return [int(n) for n in primes]


def L(n: int, x: int) -> int:
    return (x - 1) // n


# Used to specify the desired bit length of the modulus n
def create_key_pair(bit_length: int = DEFAULT_BIT_LENGTH) -> Tuple[PrivateKey, PublicKey]:
    primes = generate_primes(2**(bit_length//2))
    p = secrets.choice(primes)
    q = secrets.choice(primes)
    n = p * q
    phi = (p-1)*(q-1)
    while p==q or np.gcd(n, phi)!=1: # or n.bit_length()!=bit_length 
#       p = secrets.choice(primes)
      q = secrets.choice(primes) 
      phi = (p-1)*(q-1)
    n_squared = n ** 2
    g = secrets.randbelow(n_squared - 1) + 1
    lam = int(np.lcm(p-1, q-1))
    mu = InverseMod(L(n, pow(g, lam, n_squared)), n)
    while mu == None:
        g = secrets.randbelow(n_squared - 1) + 1
        lam = int(np.lcm(p-1, q-1))
        mu = InverseMod(L(n, pow(g, lam, n_squared)), n)
    pk = PublicKey(g, n, n_squared)
    sk = PrivateKey(lam, mu)
    return sk, pk

def encrypt(public_key: PublicKey, plaintext: int) -> int:
    g, n, n_squared = public_key
    r = secrets.randbelow(n)
    c = pow(g, plaintext, n_squared) * pow(r, n, n_squared) % n_squared
    return c

def decrypt(private_key: PrivateKey, public_key: PublicKey, ciphertext: int) -> int:
    lam, mu = private_key
    _, n, n_squared = public_key
    m = L(n, pow(ciphertext, lam, n_squared)) * mu % n
    return m


def add(public_key: PublicKey, ciphertext_a: int, ciphertext_b: int) -> int:
    return ciphertext_a * ciphertext_b % public_key.n_squared


def multiply(public_key: PublicKey, ciphertext_a: int, plaintext_b: int) -> int:
    if plaintext_b == 0:
        return encrypt(public_key, plaintext_b)
    if plaintext_b == 1:
        encrypted_0 = encrypt(public_key, 0)
        return add(public_key, ciphertext_a, encrypted_0)
    return pow(ciphertext_a, plaintext_b, public_key.n_squared)
