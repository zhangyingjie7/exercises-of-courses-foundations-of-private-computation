# coding:utf-8
'''
Created on 20211231

@author: Yingjie Zhang
Diffie-Hellman Key Exchange
'''
import matplotlib.pyplot as plt
import numpy as np
from crypto import GeneratePrimeGeneratorPair
from random import randrange
from time import time
from random import seed

def LogarithmProblem():
    xmax = 1000
    ymax = np.log10(xmax)    
    x = np.linspace(1,xmax,xmax)
    y = np.log10(x)    
    plt.clf()
    fig = plt.figure(figsize=(14,4))
    ax = fig.add_subplot(1,1,1)
    ax.plot(x,y)    
    ax.set_xticks(np.arange(0,xmax+1,xmax//10))
    ax.set_yticks(np.arange(0,ymax+1,1))    
    ax.set_title("$y=\log_{10}(x)$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")    
    plt.grid()
    plt.show()
    
def DiscreteLogarithmProblem():
    p,g = GeneratePrimeGeneratorPair(8)
    print(f"Prime number:\n\t{p}\nGenerator:\n\t{g}")
    y = np.arange(1,p)
    x = np.array([pow(g,int(y_),p) for y_ in y])
    plt.clf()
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x,y)
    ax.set_xticks(np.arange(0,p+1,p//10))
    ax.set_yticks(np.arange(0,p+1,p//10))
    ax.set_title("Discrete Logarithm")
    ax.set_xlabel("$x=g^y (mod p)$")
    ax.set_ylabel("$y$")
    plt.grid()
    plt.show()

def findY(x,p,g,max_iter):
    i = 0
    while i < max_iter:
        y = randrange(1,p)
        i += 1
        if pow(g,y,p) == x:
            return y
    return None
p, g = GeneratePrimeGeneratorPair(8)
x = randrange(p)
y = findY(x,p,g,5000000)
assert x == pow(g,y,p),"not found"
# print(x,y,p,g)
    
    
def solveDLP():
    times = []
    trials = 20
    seed(4)
    
    for bits in range(4,18,1):
        count = 1
        avg_times = []
        while count < trials:
            p,g = GeneratePrimeGeneratorPair(bits)
            x = randrange(1,p)
            t_start = time()
            y = findY(x, p, g, 9999999999)
            t_end = time()
            avg_times.append(t_end-t_start)
            count += 1
        print(f"bits: {bits}, time: {np.mean(np.array(avg_times))}")
        times.append((bits,np.mean(np.array(avg_times))))
    plt.clf()
    bits = [x[0] for x in times]
    t = [x[1] for x in times]
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(bits,t)
    ax.set_title("Time for cracking the DLP")
    ax.set_xlabel("bytes of $p$")
    ax.set_ylabel("time ($s$)")
    plt.grid()
    plt.show()


class Party():
    def __init__(self,name,p,g):
        self.name = name
        self.p = p
        self.g = g
        self.a = randrange(self.p)
        self.A = pow(self.g,self.a,self.p)
        self.s = None
    def send_A(self)->int:
        return self.A
    def get_B(self,B):
        self.s = pow(B,self.a,self.p)
    def __str__(self)->str:
        return f"Party:{self.name}\np:{self.p}\na:{self.a}\nA:{self.A}\ns:{self.s}"

bits = 16
p,g = GeneratePrimeGeneratorPair(bits)
alice = Party("Alice",p,g)
bob = Party("Bob",p,g)
print(alice)
print()
print(bob)
print()
print("---------------------------------")
A = alice.send_A()
B = bob.send_A()
print(A,B)
print()
print("---------------------------------")
alice.get_B(B)
bob.get_B(A)
print(alice)
print()
print(bob)

                