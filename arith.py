import markovify
from numpy import cumsum
from fractions import Fraction

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


    
#Suposem donat una taula de frequencies (FALTA FER)
freqTab = [1]*256


def get_next_character(f):
    """Reads one character from the given textfile"""
    c = f.read(1)
    while c: 
        yield c
        c = f.read(1)
        
        
with open("corpus.txt") as f:
    count = 0
    for c in get_next_character(f):
        count += 1
        charASCII = ord(c)
        freqTab[charASCII] += 1


#S'ha de crear una taula de frequencies acumulades
sumFreq = cumsum(freqTab)
cumFreq = [0]*257
for i in range(1, 257):
    cumFreq[i] = float(sumFreq[i - 1]) / float(sumFreq[-1])


#Suposem que tenim un input 
entrada = "havia una vez un cerdito , muy bonito que viajaba todo el dia por  el valle y un dia se encontro "
interval_inf = 0
interval_sup = 1
length = len(entrada)

for i in range(length):
    lengthInterval = interval_sup - interval_inf
    char = entrada[i]
    charASCII = ord(char)
    interval_inf = cumFreq[charASCII] * lengthInterval
    interval_sup = cumFreq[charASCII + 1] * lengthInterval

print(interval_inf)
print(interval_sup)
    




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
