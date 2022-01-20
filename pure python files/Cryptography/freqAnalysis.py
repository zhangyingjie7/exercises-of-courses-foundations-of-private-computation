# coding:utf-8
'''
Created on 20211227

@author: Yingjie Zhang

freqAnalysis of ciphertext
'''
from collections import Counter


class freqAnalysis():
    def __init__(self):
        self.english_letter_counts = [("a", 0.082),
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
        self.english_letter_counts.sort(key=lambda x: x[1],reverse=True)
        
    def letter_count(self,text):
        text2 = text.replace(" ","")
        letters = [c for c in text2]
        return Counter(letters).most_common()
    
    def getFrequencyOrder(self,message):
        letter_counts = self.letter_count(message)
        freqOrder = [v[0] for v in letter_counts]
        return ''.join(freqOrder)
    
    def englishFreqMatchScore(self,message):
        # Return the number of matches that the string in the message
        # parameter has when its letter frequency is compared to English
        # letter frequency. A "match" is how many of its six most frequent
        # and six least frequent letters is among the six most frequent and
        # six least frequent letters for English.
        freqOrder = self.getFrequencyOrder(message)
        freqEnglish = ''.join([v[0] for v in self.english_letter_counts])
        matchsocre = 0
        # Find how many matches for the six most common letters there are.
        for v in freqOrder[:6]:
            if v in freqEnglish[:6]:
                matchsocre += 1
        # Find how many matches for the six least common letters there are.   
        for v in freqOrder[-6:]:
            if v in freqEnglish[-6:]:
                matchsocre += 1
        return matchsocre
    
    
    
    
    