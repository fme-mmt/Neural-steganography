import markovify
from numpy import cumsum
from fractions import Fraction
from collections import defaultdict

text = "Example phrase. This is another example sentence. And another one"
text_model = markovify.Text(text)
chain = text_model.chain

# My initial state
from markovify.chain import BEGIN
ini_state = tuple(2* [BEGIN])



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
    fqa =cumsum(freqTab.values())
    length = len(freqTab) + 1
    cumFreq = [0] * length
    for i in range(1, length):
        cumFreq[i] = float(fqa[i - 1]) / float(fqa[-1])
    cFreq = (freqTab.keys(), cumFreq)
    return cFreq
    



    
#Suposem que tenim un input 
entrada = "maravilloso"
interval_inf = 0
interval_sup = 1
length = len(entrada)
freqTab = defaultdict(int)

fixed = True

for i in range(ord('a'), ord('z')):
    freqTab[chr(i)] = 1;
    
for i in range(ord('0'), ord('9')):
    freqTab[chr(i)] = 1;
    
    
if (fixed):
    with open("corpus.txt") as f:
        for c in get_next_character(f):
            string = str(c)
            if(string.isupper()):
                string = string.lower()
                freqTab[string] += 1
            elif (c in freqTab):
                freqTab[c] += 1
    for k, f in freqTab.items():
        if f < 500:
            del freqTab[k]
    keys,cumFreq = calculate_cum_freq(freqTab)   
    
    for i in range(length):
        lengthInterval = interval_sup - interval_inf
        char = entrada[i]
        j = keys.index(char)
      

        interval_inf = cumFreq[j] * lengthInterval
        interval_sup = cumFreq[j+ 1] * lengthInterval
        
       

else: 
    for i in range(length):
        lengthInterval = interval_sup - interval_inf
        keys, cumFreq = calculate_cum_freq(freqTab)
        char = entrada[i]
        j = keys.index(char)

        interval_inf = cumFreq[j] * lengthInterval
        interval_sup = cumFreq[j + 1] * lengthInterval
        

     
print(interval_inf)
print(interval_sup)
print((interval_inf + interval_sup) / 2.)
    
    
valor_entrada = find_fraction(interval_inf, interval_sup)

print(valor_entrada)



chain.walk((BEGIN, 'This'))
# Gives: ['is', 'another', 'example', 'sentence.']

chain.walk(('This', 'is'))
# Gives: ['another', 'example', 'sentence.']

chain.move(('This', 'is'))
# Gives: 'another'

chain.model[ini_state]
# Gives: {'Example': 1, 'This': 1}

from numpy import cumsum

choices, weigths = zip(*chain.model[ini_state].items())
sw = cumsum(weigths)
print(sw/sw[-1])
print(choices)
