# coding:utf-8
'''
Created on 20211220

@author: Yingjie Zhang

Shift Cipher, Attack on shift Cipher
'''

import string
from random import randrange, seed

# print(f"These are ascii lowercase we will use for our messages:\n\t{string.ascii_lowercase}")

class ShiftCipher:
    def shift_by(self,secret_key: str) -> str:
        assert len(secret_key)==1, "secret key must be lenght 1"
        assert secret_key in string.ascii_lowercase, f"{secret_key} is not ascii lowercase"
        
        int_key = ord(secret_key) - ord('a')
        
        return string.ascii_lowercase[int_key:] + string.ascii_lowercase[:int_key] 
    
    def testShift_by(self):
        print(f"alphabet:\n\t{string.ascii_lowercase}")
        print(f"ceasar encrypted alphabet\n\t{self.shift_by('d')}")
        
    def shift_encrypt(self, plaintext: str, secret_key: str) -> str:
        shifted = self.shift_by(secret_key)
        convert_dict = {p:c for p,c in zip(string.ascii_lowercase,shifted)}
        convert_dict[" "] = " "
        return ''.join([convert_dict[p] for p in plaintext])
    
    def shift_decrypt(self, ciphertext: str, secret_key: str) -> str:
        shifted = self.shift_by(secret_key)
        convert_dict = {c:p for p,c in zip(string.ascii_lowercase,shifted)}
        convert_dict[" "] = " "
        return ''.join([convert_dict[c] for c in ciphertext])
    
    def shift_cipher(self, text:str, secret_key: str, encrypt: bool = True) -> str:
        shifted = self.shift_by(secret_key)
        if encrypt:
            convert_dict = {p:c for p,c in zip(string.ascii_lowercase,shifted)}
        else:
            convert_dict = {c:p for p,c in zip(string.ascii_lowercase,shifted)}
        
        convert_dict[" "] = " "
        return ''.join([convert_dict[c] for c in text])
    
    def random_attack(self):
        seed(4)
        secret_key = string.ascii_lowercase[randrange(len(string.ascii_lowercase))]
        message = "this is a message"
        encrypted_message = self.shift_cipher(message,secret_key,True)
        print(f"secret_key:\n\t{secret_key}")
        print(f"message:\n\t{message}")
        print(f"encrypted_message:\n\t{encrypted_message}\n\n")
        
        for possible_key in string.ascii_lowercase:
            decrypted_message = self.shift_cipher(encrypted_message,possible_key,False)
            print(f"Decrypted message for key {possible_key}:\n\t{decrypted_message}")
        
        

Test = ShiftCipher()
message = "this is a secret message"
encrypted_message = Test.shift_cipher(message, "c", True)
decrypted_message = Test.shift_cipher(encrypted_message, "c", False)
print(f"Original message is: \n\t{message}")
print(f"Ciphertext is: \n\t{encrypted_message}")
print(f"Decrypted message is: \n\t{decrypted_message}")

print()
Test.random_attack()
