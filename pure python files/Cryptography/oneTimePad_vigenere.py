'''
Created on 20211222
# coding:utf-8
@author: Yingjie Zhang

One Time Pad based on Vigenere Cipher
'''
from vigenere_cipher import *
from copy import deepcopy
from utils import process_load_textfile
from collections import Counter
from typing import List, Tuple
import matplotlib.pyplot as plt
from Cryptography.vigenere_cipher import VigenereCipher


download_path =  'data/'
filename = 'Nineteen-eighty-four_Orwell.txt'
data = process_load_textfile(filename, download_path)

print("Test data:\n\t",data[10000:11000])
print()

def letter_count(text:str)-> List[Tuple[str,int]]:
    text2 = text.replace(" ","")
    letters = [c for c in text2]
    return Counter(letters).most_common()
freq = letter_count(data)
print("The frequency for the book nineteen eighty four:\n\t",freq)
print()

def freq_plotter(text:str,title:str)->plt:
#     plt.clf()
    freq = letter_count(text)
    names = [x[0] for x in freq]
    values = [x[1] for x in freq]
    fig = plt.figure(figsize=(16,7))
    plt.bar(names,values)
    plt.title(title)
    plt.show(fig)
    plt.close(fig)
    return fig

freq_plotter(data, "Frequencies of letters for Nineteen Eighty Four")

# A function that randomly draws a random portion of the text
def draw_sample(text:str,size:int)->str:
    n = len(text)
    i_init = randrange(n)
    i_final = i_init+size
    c = ''
    for i in range(i_init,i_final):
        c += text[i%n]
    return c

seed(3)
text_c = draw_sample(data,100)
print("100 random bits of the book:\n\t",text_c)
print()

# Counting frequencies with short key(Vigenere with key size 1)
seed(10)
message_size = len(data)
secret_key_size = message_size
print("message_size = ",message_size,"\nsecret_key_size = ",secret_key_size)

V = VigenereCipher()
message = draw_sample(data, message_size) # generating random message, we use all of the data
secret_key = V.vigenere_key_generator(secret_key_size) # generating secret key
ciphertext = V.vigenere_encrypt_decrypt(message, secret_key, encrypt=True) # calculating ciphertext that Alice sends to Bob
print("THE SECRET KEY: \n\t",secret_key)
assert message == V.vigenere_encrypt_decrypt(ciphertext,secret_key,encrypt=False), "something went wrong" # just to make sure Vigenere is well coded
fig = freq_plotter(ciphertext, "Frequencies for ciphertext size " + str(message_size)+ " and key size "+str(secret_key_size))





