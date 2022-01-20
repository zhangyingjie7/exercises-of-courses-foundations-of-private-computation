# coding:utf-8
'''
Created on 20211220

@author: Yingjie Zhang

Vigenere Cipher
'''
import string
from random import randrange, seed
from Cryptography.utils import download_data, process_load_textfile


class VigenereCipher():
    def vigenere_key_generator(self, secret_key_size: int) -> str:
        n = len(string.ascii_lowercase)
        secret_key = ''
        while len(secret_key) < secret_key_size:
            secret_key +=string.ascii_lowercase[randrange(n)]
        return secret_key
    
    def shift_letter(self, letter: str, shiftby: str, forward: bool=True) -> str:
        n = len(string.ascii_lowercase)
        letter_int = ord(letter) - ord('a')
        shiftby_int = ord(shiftby) - ord('a')
        if forward:
            return string.ascii_lowercase[(letter_int+shiftby_int)%n]
        else:
            return string.ascii_lowercase[(letter_int-shiftby_int)%n]
    
    def vigenere_encrypt_decrypt(self,message: str, secret_key: str, encrypt:bool = True) -> str:
        key_len = len(secret_key)
        encoded = ''
        for i,letter in enumerate(message):
            if letter in string.ascii_lowercase:
                encoded += self.shift_letter(letter, secret_key[i%key_len], forward=encrypt)
            else:
                encoded += letter
        return encoded

def main():
    T = VigenereCipher()
#     secret_key_size = 5
#     secret_key = T.vigenere_key_generator(secret_key_size)
# #     secret_key = 'gift'
#     sentence = 'cryptography is a cool subject'
#     ciphertext = T.vigenere_encrypt_decrypt(sentence, secret_key, True)
#     plaintext = T.vigenere_encrypt_decrypt(ciphertext, secret_key, False)
#     print("THE SECRET KEY: \n\t",secret_key,"\nTHE SENTENCE:\n\t",sentence,"\nCIPHERTEXT:\n\t",ciphertext,"\nPLAINTEXT:\n\t",plaintext)
#     print()
    
    filename = 'Nineteen-eighty-four_Orwell.txt'
    filepath =  'data/'
    data = process_load_textfile(filename, filepath)
    secret_key_size = 5
    secret_key = T.vigenere_key_generator(secret_key_size)
    print(secret_key)  # decll
    ciphertext = T.vigenere_encrypt_decrypt(data, secret_key, True)
    myfile = open('data/Vigenere_ciphertext.txt','w')
    print(ciphertext,file = myfile,end='')
    
# main()