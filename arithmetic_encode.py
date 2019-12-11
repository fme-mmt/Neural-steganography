from numpy import cumsum
from collections import defaultdict
from mpmath import mpf, mp

mp.dps = 50


def get_next_character(f):
    """Reads one character from the given textfile"""
    c = f.read(1)
    while c: 
        yield c
        c = f.read(1)

def calculate_cum_freq(freqTab):
    fqa = cumsum(list(freqTab.values()))
    length = len(freqTab) + 1
    cumFreq = [0] * length
    for i in range(1, length):
        cumFreq[i] = mpf(float(fqa[i - 1]) / float(fqa[-1]))
    cFreq = (list(freqTab.keys()), cumFreq)
    return cFreq
    

def arithmetic_encode (word, fixed):
    interval_inf = 0
    interval_sup = 1
    length = len(word)
    freqTab = defaultdict(int)


    for i in range(ord('a'), ord('z') + 1):
        freqTab[chr(i)] = 1;
        
    for i in range(ord('A'), ord('Z') + 1):
        freqTab[chr(i)] = 1;

    for i in range(ord('0'), ord('9') + 1):
        freqTab[chr(i)] = 1;
        
    freqTab['!'] = 1

    if (fixed):
        with open("corpus.txt") as f:
            for c in get_next_character(f):
                if (c in freqTab):
                    freqTab[c] += 1
           
    keys, cumFreq = calculate_cum_freq(freqTab)
    print(cumFreq)
    print(' ')
    for i in range(length):
        char = word[i]
        lengthInterval = mpf(interval_sup - interval_inf)
        j = keys.index(char)
        interval_sup = mpf(cumFreq[j + 1]*lengthInterval + interval_inf)
        interval_inf = mpf(cumFreq[j]*lengthInterval + interval_inf)
        print(interval_inf)
        print(interval_sup)
        print(' ')
        if (not fixed): 
            freqTab[char] += 1
            keys, cumFreq = calculate_cum_freq(freqTab)

    return mpf((interval_inf + interval_sup)/2)



    
def arithmetic_decode(number, fixed):

    freqTab = defaultdict(int)
    
    
    for i in range(ord('a'), ord('z') + 1):
        freqTab[chr(i)] = 1;
        
    for i in range(ord('A'), ord('Z') + 1):
        freqTab[chr(i)] = 1;

    for i in range(ord('0'), ord('9') + 1):
        freqTab[chr(i)] = 1;
        
    freqTab['!'] = 1
        
    if (fixed):
        with open("corpus.txt") as f:
            for c in get_next_character(f):
                if (c in freqTab):
                    freqTab[c] += 1
      
    keys, cumFreq = calculate_cum_freq(freqTab)
    lengthInterval = 1
    interval_inf = 0
    interval_sup = 1
    s = ''
    trobat = False
    count = 1
    while (not trobat and count < 25):
        count += 1
        i = 0
        while (number > (interval_inf + lengthInterval * cumFreq[i]) and i < len(keys) - 1): i += 1
        if(i == len(keys) - 1): trobat = True
        interval_sup = cumFreq[i]*lengthInterval + interval_inf
        interval_inf = cumFreq[i - 1]*lengthInterval + interval_inf
        lengthInterval = interval_sup - interval_inf
        if (not trobat):
            char = keys[i - 1]
            s += char
        if (not fixed):
            freqTab[char] += 1
            keys, cumFreq = calculate_cum_freq(freqTab)
    return s;
	

secret_message = "CaYXSSaLS235743!"
n=arithmetic_encode(secret_message,False) 
print(n)


arithmetic_decode(n, False)


    