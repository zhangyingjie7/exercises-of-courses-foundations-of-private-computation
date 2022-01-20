# coding:utf-8
'''
Created on 20211226

@author: Yingjie Zhang

Attack Vigenere Cipher 
Babbage Attack: any key
'''

import itertools, re
import string
from Cryptography.vigenere_cipher import VigenereCipher
from Cryptography.freqAnalysis import freqAnalysis
from Cryptography.VigenereDictionaryAttack import detectEnglish

class BabbageAttack():
    def __init__(self):
        self.LOWERLETTERS = string.ascii_lowercase
        self.NUM_MOST_FREQ_LETTERS = 4 # attempts this many letters per subkey
        self.MAX_KEY_LENGTH  = 5 # will not attempt keys longer than this
        self.NONLETTERS_PATTERN = re.compile('[^a-z]')
        self.min_lettersequences = 3
        self.max_lettersequences = 5
    
    def findRepeatSequencesSpacings(self,message):
        # Goes through the message and finds any self.min_lettersequences to 
        # self.max_lettersequences letter sequences
        # that are repeated. Returns a dict with the keys of the sequence and
        # values of a list of spacings (num of letters between the repeats).
        
        # Use a regular expression to remove non-letters from the message.
        message = self.NONLETTERS_PATTERN.sub('',message.lower())
        seqSpacings = {} # keys are sequences, values are list of int spacings
        for seqLen in range(self.min_lettersequences,self.max_lettersequences+1):
            for seqStart in range(len(message)-seqLen):
                # Determine what the sequence is, and store it in seq
                seq = message[seqStart:seqStart+seqLen]
                
                # Look for this sequence in the rest of the message
                for i in range(seqStart+seqLen,len(message)-seqLen):
                    if message[i:i+seqLen] == seq:
                        # Found a repeated sequence.
                        if seq not in seqSpacings:
                            seqSpacings[seq] = [] # initialize blank list
                        
                        # Append the spacing distance between the repeated sequence and the original sequence.
                        seqSpacings[seq].append(i-seqStart)
        return seqSpacings
    
    def getUsefulFactors(self,num):
        # Returns a list of useful factors of num. By "useful" we mean factors
        # less than MAX_KEY_LENGTH + 1. For example, getUsefulFactors(144)
        # returns [2, 72, 3, 48, 4, 36, 6, 24, 8, 18, 9, 16, 12]
        if num < 2:
            return []
        factors = []
        for i in range(2,self.MAX_KEY_LENGTH+1):
            if num % i ==0:
                factors += [i]
                factors += [int(num/i)]
        if 1 in factors:
            factors.remove(1)
        return list(set(factors))

    def getMostCommonFactors(self,seqFactors):
        # First, get a count of how many times a factor occurs in seqFactors.
        factorCounts = {} # key is a factor, value is how often if occurs
        
        # seqFactors keys are sequences, values are lists of factors of the
        # spacings. seqFactors has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
        # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
        for seq in seqFactors:
            factorList = seqFactors[seq]
            for factor in factorList:
                if factor not in factorCounts:
                    factorCounts[factor] = 0
                factorCounts[factor] += 1
        # Second, put the factor and its count into a tuple, and make a list
        # of these tuples so we can sort them.
        factorsByCount = []
        for factor in factorCounts:
            # exclude factors larger than MAX_KEY_LENGTH
            if factor <= self.MAX_KEY_LENGTH:
                # factorsByCount is a list of tuples: (factor, factorCount)
                # factorsByCount has a value like: [(3, 497), (2, 487), ...]
                factorsByCount.append((factor,factorCounts[factor]))
        # Sort the list by the factor count.
        factorsByCount.sort(key=lambda x:x[1],reverse=True)
        return factorsByCount
    
    def kasiskiExamination(self,ciphertext):
        # Find out the sequences of 3 to 5 letters that occur multiple times
        # in the ciphertext. repeatedSeqSpacings has a value like:
        # {'EXG': [192], 'NAF': [339, 972, 633], ... }
        repeatedSeqSpacings = self.findRepeatSequencesSpacings(ciphertext)
        
        seqFactors = {}
        for seq in repeatedSeqSpacings:
            seqFactors[seq] = []
            for spacing in repeatedSeqSpacings[seq]:
                seqFactors[seq].extend(self.getUsefulFactors(spacing))
        
        factorsByCount = self.getMostCommonFactors(seqFactors)
        # Now we extract the factor counts from factorsByCount and
        # put them in allLikelyKeyLengths so that they are easier to
        # use later.
        allLikelyKeyLengths = []
        for factor in factorsByCount:
            allLikelyKeyLengths.append(factor[0])
        return allLikelyKeyLengths
    
    def getNthSubkeysLetters(self,n, keyLength, message):
        # Returns every Nth letter for each keyLength set of letters in text.
        # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'aaa'
        #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'bbb'
        #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'ccc'
        #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'af'
        
        # Use a regular expression to remove non-letters from the message.
        message = message.lower()
        message = self.NONLETTERS_PATTERN.sub('',message)
        i = n-1
        letters = []
        while i <len(message):
            letters.append(message[i])
            i += keyLength
        return ''.join(letters)
    
    def attemptHackWithKeyLength(self,ciphertext, mostLikelyKeyLength): 
        # Determine the most likely letters for each letter in the key.   
        ciphertextLower = ciphertext.lower()
        # allFreqScores is a list of mostLikelyKeyLength number of lists.
        # These inner lists are the freqScores lists.
        allFreqScores = []
        F = freqAnalysis()
        V = VigenereCipher()
        D = detectEnglish()
        for nth in range(1,mostLikelyKeyLength+1):
            nthLetters = self.getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextLower)
            
            # freqScores is a list of tuples like:
            # [(<letter>, <Eng. Freq. match score>), ... ]
            # List is sorted by match score. Higher score means better match.
            freqScores = []
            for possibleKey in self.LOWERLETTERS:
                decryptedText = V.vigenere_encrypt_decrypt(nthLetters,possibleKey,False)
                keyAndFreqMatchTuple = (possibleKey,F.englishFreqMatchScore(decryptedText))
                freqScores.append(keyAndFreqMatchTuple) 
            freqScores.sort(key=lambda x:x[1], reverse=True)
            allFreqScores.append(freqScores[:self.NUM_MOST_FREQ_LETTERS])
        
        for i in range(len(allFreqScores)):
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()
        
        # Try every combination of the most likely letters for each position
        # in the key.
        for indexes in itertools.product(range(self.NUM_MOST_FREQ_LETTERS), \
                                         repeat=mostLikelyKeyLength):
            # self.NUM_MOST_FREQ_LETTERS ^ mostLikelyKeyLength
            possibleKey = ''
            for i in range(mostLikelyKeyLength):
                possibleKey += allFreqScores[i][indexes[i]][0]
            print('Attempting with key: %s' % (possibleKey))
            decryptedText = V.vigenere_encrypt_decrypt(ciphertextLower,possibleKey,False)
            if (D.isEnglish(decryptedText, wordPercentage=50, letterPercentage=85)):
                # Set the hacked ciphertext to the original casing.
                oriCase = []
                for i in range(len(ciphertext)):
                    if ciphertext[i].isupper():
                        oriCase.append(decryptedText[i].upper())
                    else:
                        oriCase.append(decryptedText[i].lower())
                decryptedText = ''.join(oriCase)
                print('Possible encryption hack with key %s:' % (possibleKey))
                print(decryptedText[:200]) 
                return decryptedText
            
        # No English-looking decryption found, so return None.
        return None
        
                
    def hackVigenere(self,cipherText):
        # First, we need to do Kasiski Examination to figure out what the
        # length of the ciphertext's encryption key is.
        allLikelyKeyLengths = self.kasiskiExamination(cipherText)
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
        
        for keyLength in allLikelyKeyLengths:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, self.NUM_MOST_FREQ_LETTERS ** keyLength))
            hackedMessage = self.attemptHackWithKeyLength(cipherText, keyLength)
            if hackedMessage != None:
                break
        # If none of the key lengths we found using Kasiski Examination
        # worked, start brute-forcing through key lengths.
        if hackedMessage == None:
            print('Unable to hack message with likely key length(s). Brute-forcing key length...')
            for keyLength in range(1, self.MAX_KEY_LENGTH + 1):
                if keyLength not in allLikelyKeyLengths:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, self.NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = self.attemptHackWithKeyLength(cipherText, keyLength)    
                if hackedMessage != None:
                    break
        return hackedMessage

def main():
    ciphertext = open('data/Vigenere_ciphertext.txt').read()[:9000]
    plaintext_file = open('data/Vigenere_plaintext.txt','w')
    B = BabbageAttack()
    plaintext = B.hackVigenere(ciphertext)
    if plaintext != None:
        print(plaintext,file=plaintext_file)
    else:
        print('Failed to hack encryption.')

main()
