
import markovify
import numpy as np
from numpy import cumsum
from markovify.chain import BEGIN,END
from fractions import Fraction
from collections import defaultdict

def find_fraction(input_start, input_end):
    output_fraction = Fraction(0, 1)
    output_denominator = 1

    input_start_fraction = Fraction(input_start)
    input_numerator = input_start_fraction.numerator
    input_denominator = input_start_fraction.denominator

    while not (input_start <= float(output_fraction) < input_end):

        output_numerator = 1 + ((input_numerator * output_denominator) // input_denominator)
        output_fraction = Fraction(output_numerator, output_denominator)
        output_denominator *= 2

    return output_fraction



def get_next_character(f):
    """Reads one character from the given textfile"""
    c = f.read(1)
    while c: 
        yield c
        c = f.read(1)

def calculate_cum_freq(freqTab):
    fqa =cumsum(list(freqTab.values()))
    length = len(freqTab) + 1
    cumFreq = [0] * length
    for i in range(1, length):
        cumFreq[i] = float(fqa[i - 1]) / float(fqa[-1])
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
    for i in range(length):
        char = word[i]
        lengthInterval = interval_sup - interval_inf
        j = keys.index(char)
        interval_sup = cumFreq[j + 1]*lengthInterval + interval_inf
        interval_inf = cumFreq[j]*lengthInterval + interval_inf
        if (not fixed): 
            freqTab[char] += 1
            keys, cumFreq = calculate_cum_freq(freqTab)
                
    return (interval_inf + interval_sup)/2



    
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
    while (not trobat and count < 9):
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
	
def carrega():
    with open('corpus.txt') as f: #indicar be on esta el corpus
        text = f.read()
    return markovify.Text(text,state_size = 4).chain
chain=carrega()

def move(state, w):
    return state[1:] + (w,)

def cumfreqs(chain, state):
    choices, weights = zip(*chain.model[state].items())
    sw = np.cumsum(np.array(weights, dtype=float))
    sw /= sw[-1]
    return (choices, np.concatenate(([0], sw)))

secret_message = "WWWWZ834!"
init_state = 4*(BEGIN,) #El numero depen de state_size
n=arithmetic_encode(secret_message,False) #Numero que surt de l'Arithmetic coding. 9 decimals funciona guai
print(n)
message = arithmetic_decode(n,False)
print(message)

word = 'BEGIN'
while word != END:
    chs, fq = cumfreqs(chain, init_state)
    for i in range(len(fq)-1):
        if fq[i] <= n < fq[i+1]: break
    #fq[i], fq[i+1], chs[i]
    #Actulaitzem pel seguent pas
    init_state = move(init_state, chs[i])
    n = (n - fq[i])/float(fq[i+1]-fq[i])
    word = chs[i]
    print(word)