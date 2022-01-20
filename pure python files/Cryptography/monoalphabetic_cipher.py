# coding:utf-8
'''
Created on 20211220

@author: Yingjie Zhang

Mono alphabetic Cipher, Attack on Mono alphabetic Cipher
'''
from copy import deepcopy
import string
from random import randrange, seed
import os
import requests

from utils import download_data, process_load_textfile
from collections import Counter
from typing import List, Tuple


class MonoalphabeticCipher:
    def mono_key_generator(self) -> str:
        chars = list(deepcopy(string.ascii_lowercase))
        chars_permutation = []
        while len(chars)>0:
            letter = chars.pop(randrange(len(chars)))
            chars_permutation.append(letter)
        return ''.join(chars_permutation)
    
    def mono_encrypt_decrypt(self,text: str, secret_key: str, encrypt: bool=True) -> str:
        if encrypt:
            convert_dict = {p:c for p, c in zip(string.ascii_lowercase, secret_key)}
        else:
            convert_dict = {c:p for p, c in zip(string.ascii_lowercase, secret_key)}
        convert_dict[" "] = " "
        return ''.join(convert_dict[c] for c in text)
    
    
    def letter_count(self,text:str)-> List[Tuple[str,int]]:
        text2 = text.replace(" ","")
        letters = [c for c in text2]
        return Counter(letters).most_common()
    

    def doloadDataEnc(self):

        url = 'http://gutenberg.net.au/ebooks01/0100021.txt'
        filename = 'Nineteen-eighty-four_Orwell.txt'
        download_path =  'data/' # '/'.join(os.getcwd().split('/')[:-1]) +
        #download data to specified path
        download_data(url, filename, download_path)
        
        #load data and process
        data = process_load_textfile(filename, download_path)
        print("Test print data:\n\t",data[10000:11000])
        
        lc = self.letter_count(data)
        print("Test data letter count:\n\t",lc)
        
        # key generation
        secret_key = self.mono_key_generator()
        
        # message
        data_len = len(data)
        init_letter = data_len//2
        final_letter = init_letter + data_len//4
        message = data[init_letter:final_letter]
        # message encryption 
        encrypted_message = self.mono_encrypt_decrypt(message, secret_key,True)
        return message,encrypted_message,secret_key
    
    def known_ciphertext_attack(self,encrypted_message:str)->str:
        english_letter_counts = [("a", 0.082),
                         ("b", 0.015),
                         ("c", 0.028),
                         ("d", 0.043),
                         ("e", 0.13),
                         ("f", 0.022),
                         ("g", 0.02),
                         ("h", 0.061),
                         ("i", 0.07),
                         ("j", 0.0015),
                         ("k", 0.0077),
                         ("l", 0.04),
                         ("m", 0.024),
                         ("n", 0.067),
                         ("o", 0.075),
                         ("p", 0.019),
                         ("q", 0.00095),
                         ("r", 0.06),
                         ("s", 0.063),
                         ("t", 0.091),
                         ("u", 0.028),
                         ("v", 0.0098),
                         ("w", 0.024),
                         ("x", 0.0015),
                         ("y", 0.002),
                         ("z", 0.00074)]
        # sort them according to their frequency
        english_letter_counts.sort(key=lambda x: x[1],reverse=True)
        characters = string.ascii_lowercase
        ciphertext_letter_frequencies = self.letter_count(encrypted_message)
        ciphertext_letter_frequencies.sort(key=lambda x: x[1],reverse=True)
        key_dict = {}
        for (english_letter,_),(ctx_letter,_) in zip(english_letter_counts,ciphertext_letter_frequencies):
            if key_dict.get(english_letter) is None:
                key_dict[english_letter] = ctx_letter
        inferred_secret_key = [key_dict[letter] if key_dict.get(letter) is not None else "_" for letter in characters]
        return ''.join(inferred_secret_key)        

# Test1
def testEncDec():
    T = MonoalphabeticCipher()
    seed(5)
    
    # generate a random secret key for mono alphabetic
    secret_key = T.mono_key_generator()
    
    # sentence to encrypt and ciphertext
    sentence = "cryptography is a cool subject"
    ciphertext = T.mono_encrypt_decrypt(sentence, secret_key)
    plaintext = T.mono_encrypt_decrypt(ciphertext, secret_key, encrypt=False)
    
    print("THE SECRET KEY: \n\t",secret_key,"\nTHE SENTENCE:\n\t",sentence,"\nCIPHERTEXT:\n\t",ciphertext,"\nPLAINTEXT:\n\t",plaintext)


# Test2
def TestdoloadDataEnc():
    T = MonoalphabeticCipher()
    seed(2)
    T.doloadDataEnc()

# Test3   
def TestAttack():
    T = MonoalphabeticCipher()
    seed(2)
    message,encrypted_message,secret_key = T.doloadDataEnc()
    guessed_secret_key = T.known_ciphertext_attack(encrypted_message)
    
    print("Orgin key:\n\t",secret_key)
    print("Guessed key:\n\t",guessed_secret_key)
    
    correct_geuss_count = 0
    for sk,guess_sk in zip(secret_key,guessed_secret_key):
        if sk == guess_sk:
            correct_geuss_count = correct_geuss_count + 1
    print("Correctly guessed",correct_geuss_count,"out of",len(secret_key))
    
    guessed_message = T.mono_encrypt_decrypt(encrypted_message, guessed_secret_key, False)
    print(guessed_message[0:500])
    
    
# TestdoloadDataEnc()
# testEncDec()
TestAttack()