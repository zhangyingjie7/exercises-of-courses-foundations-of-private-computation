'''
Created on 20211227

@author: Yingjie Zhang

Modular Algebra
'''
from mpmath.libmp.libintmath import isprime

# 1.1 Modular Arithmetic
m = 6 
for i in range(2*m):
    print("i="+str(i),str(i)+"(mod "+str(m)+")="+str(i%m))
print()

# 1.2 Modular Addition
m = 6
j = 3
for i in range(m):
    print(f"{i}+{j}(mod {m}), sum = {(i+j)%m}")
print()

# 2 The Group of the Modular Sum Operations
# Associativity
m = 7
i,j,k = 3,5,2
assert ((i+j)%m+k)%m == (i+(j+k)%m)%m
# Existence of identity
m = 7
i,e =4,0
assert ((i+e)%m == i%m)
#Inverse Element
m = 7
i = 3
i_inv = m-i
assert (i+i_inv)%m ==0

# 2.1 Cyclic Groups
m = 8
g = 1 # Generator
prev_power = g
for count in range(m):
    prev_power = (prev_power + g) % m
    print(f"{g}^{count}={prev_power}") 
print()

# 2.2 Multiplicative Groups
# Associativity
m = 7
i,j,k = 2,3,5
assert (i*(j*k)%m)%m==((i*j)%m)*k%m
# Existence of identity
i,e = 3,1
assert (i*e)%m == i%m
#Inverse Element
m = 7 # Prime Number
i = 2
for j in range(m):
    print(f"{i}*{j}={(i*j)%m}")
print()

# 3. Common divisor and GCD

# 3.1 Divisor
from typing import List
def divisor(a: int) -> List[int]:
    div = []
    for i in range(1,a//2+1):
        if a%i == 0:
            div.append(i)
    return div
print(divisor(2024))
print(divisor(748))
print()
# 3.2 Euclidean Alg 
def gcd(a:int,b:int)->int:
    r0,r1 = (a,b) if a>b else (b,a)
    while r1!=0:
        r = r0%r1
        r0 = r1
        r1 = r
    return r0
print(gcd(2024,748))
print()
# 3.3 Extended Euclidean Alg
# au+bv=gcd(a,b)
def xgcd(a,b):
    if b==0:
        return a,1,0
    else:
        g,u,v = xgcd(b,a%b)
        quotient = a//b
        return g,v,(u-quotient*v)    
a = 15488710 
b = 79991630
g,u,v = xgcd(a, b) 
print(f"({u}*{a})+({v}*{b})={g}")
print()

#3.4 Multiplication Inverse
def InverseMod(a,m):
    g,u,_ = xgcd(a,m)
    if g!=1:
        print(f"{a} has no inverse modulo {m} in multiplication")
        return None
    else:
        return u%m
m = 7
a = 4
a_ = InverseMod(a,m) 
print(f"m={m},a={a},a_inverse={a_}")
print()

# 5.3.1 Expected Prime Numbers
from numpy import log
n2 = 1000000
n1 = 100000
def expectedPrimes(x):
    return x/log(x)
print(f"Expected number of primes between {n2} and {n1} is {expectedPrimes(n2)-expectedPrimes(n1)}")
print()

# 5.3.2 Sieve of Eratosthenes
def PrimeSieveEratosthenes(limit):
    a = [True]*limit
    a[0] = a[1] = False
    for i,isprime in enumerate(a):
        if isprime:
            yield i
            for n in range(i*i,limit,i):
                a[n] = False
a = list(PrimeSieveEratosthenes(100))
print(a)
print()

# 5.3.3 Verify
all_primes = list(PrimeSieveEratosthenes(n2))
primes_between = []
for prime in all_primes:
    if prime < n2 and prime>n1:
        primes_between.append(prime)
print(f"Number of primes between {n2} and {n1} is {len(primes_between)}")
print()

# 5.4 Fermat's Little Theorem Inverse
def InverseFermat(a,p):
    return pow(a,p-2,p)
print(InverseFermat(4,7))
print(f"{4*InverseFermat(4,7)%7}")
print()

# 5.5 Primality Test
# 5.5.1 First Attempt
n = 561
for a in range(n):
    if pow(a,n,n) !=a:
        print(a,pow(a,n,n))
print("pass")
print(f"Remainder of {n} divided by {3} is {n%3}")
print()

# 5.5.2 Miller Rabin Test
def isWitness(a,n,q,k):
    x = pow(a,q,n)
    if x == 1:
        return False
    for _ in range(k):
        if (x+1)%n == 0:
            return False
        x = pow(x,2,n)
    return True
from random import randrange
def isPrime(n,r):
    # Miller Rabin Test
    # n: number to test Primality
    # r: times to run the test
    if n<2:
        return False
    if n==2:
        return True
    if n%2==0:
        return False
    q = n-1
    k = 0
    while q%2 == 0:
        q = q//2
        k += 1
    assert n-1==pow(2,k)*q
    for _ in range(r):
        a = randrange(2,n)
        if isWitness(a,n,q,k):
            return False
    return True

print(isPrime(1501053443,10))
print()

# 5.6 Mersenne Primes
import math
def MersenneTest(n):
    k = None
    for i in range(n):
        isP = isPrime((pow(2,i)-1),50)
        if isP:
            k = i
    return k
p = MersenneTest(1001)
print(f"The maximum n smaller than 1000 such that 2^n-1 is a prime number is {p}")
d = math.ceil(math.log10(pow(2,p)-1))
print(f"This prime number have {d} digits")
print(f"Express the prime number in binary form, we get {p} 1's")
print()

# 6. Factorization of Composite Numbers
SMALL_PRIMES = list(PrimeSieveEratosthenes(500000))
def BruteForceFactorisation(n):
    primes=SMALL_PRIMES
    if isPrime(n,40):
        return [n],[1]
    factors = []
    reps = []
    for prime in primes:
        if n%prime ==0:
            factors.append(prime)
            reps.append(0)
            while n%prime ==0:
                n //= prime
                reps[-1] += 1
    assert n==1,"Cannot factor, primes list is too short"
    return factors,reps
n = 285587
facts,reps = BruteForceFactorisation(285587)
print(facts,reps)
n1 = 1
for p,r in zip(facts,reps):
    n1 *= p**r
if n1==n:
    print("Pass correctness verification") 
print()
    
# 6. Group Generators
from crypto import GeneratePrimeGeneratorPair
p,g = GeneratePrimeGeneratorPair(16)
print(f"Prime Number:\n\t{p}\nGenerator \n\t{g}")
group_elements = [1]
for _ in range(p-2):
    group_elements.append(group_elements[-1]*g%p)
n_elems = len(set(group_elements))
print(f"Generate {n_elems} elements")
