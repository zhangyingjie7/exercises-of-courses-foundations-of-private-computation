# coding:utf-8
'''
Created on 20211225

@author: Yingjie Zhang

Attack Vigenere Cipher 
dictionaryAttack: when the key was a word that can be found in the dictionary 
'''
from Cryptography.vigenere_cipher import VigenereCipher

class detectEnglish():
    def __init__(self):
        self.UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.LETTERS_AND_SPACE = self.UPPERLETTERS + self.UPPERLETTERS.lower() + ' \t\n'
        self.ENGLISH_WORDS = self.loadDictionary()
        
    def loadDictionary(self):
        dictionaryFile = open('dictionary.txt')
        englishWords = []
        for word in dictionaryFile.read().split('\n'):
            englishWords = englishWords + [word.lower()] # English words in lower case
        dictionaryFile.close()
        return englishWords
    
    def removeNonLetters(self,message):
        lettersOnly = []
        for symbol in message:
            if symbol in self.LETTERS_AND_SPACE:
                lettersOnly.append(symbol)
        return ''.join(lettersOnly) 
    
    def getEnglishCount(self,message):
        message = message.lower()
        message = self.removeNonLetters(message)
        possibleWords = message.split()
        if possibleWords == []:
            return 0.0  # no words at all, so return 0.0
        matches = 0
        for word in possibleWords:
            if word in self.ENGLISH_WORDS:
                matches += 1
        return float(matches)/len(possibleWords)
    
    def isEnglish(self,message,wordPercentage, letterPercentage):
        # By default, 20% of the words must exist in the dictionary file, and
        # 85% of all the characters in the message must be letters or spaces
        # (not punctuation or numbers).
        wordsMatch = (self.getEnglishCount(message)*100 >= wordPercentage)
        numLetters = len(self.removeNonLetters(message))
        messageLettersPercentage = float(numLetters) / len(message) * 100
        lettersMatch = (messageLettersPercentage >= letterPercentage)
#         print(wordsMatch,lettersMatch)
        return (wordsMatch and lettersMatch)
        

def dictionaryAttack(ciphertext): 
    # when the key was a word that can be found in the dictionary
    f = open("dictionary.txt")
    words = f.readlines()
    f.close()
    Vigenere = VigenereCipher()
    dE = detectEnglish()
    for word in words:
        word = word.strip() # remove the newline at the end
        word = word.lower()
        decryptedText = Vigenere.vigenere_encrypt_decrypt(ciphertext, word, False)
        if dE.isEnglish(decryptedText,wordPercentage=30,letterPercentage=85):
            print()
            print("Possible encryption break:")
            print("Key",str(word),":",decryptedText)
#             print()
#             print('Enter D for done, or just press Enter to continue breaking:')
#             response = input('> ')
#             if response.upper().startswith('D'):
            return decryptedText            

def main():
    ciphertext = "izdizwlkgxmr qx g hhut lajoxib"
    dictionaryAttack(ciphertext)
    
# main()     