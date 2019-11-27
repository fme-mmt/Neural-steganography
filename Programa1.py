import markovify
import numpy as np
from markovify.chain import BEGIN,END

def carrega():
    with open('corpus.txt', encoding='utf8') as f:
        text = f.read()
    return markovify.Text(text).chain
chain=carrega()

def move(state, w):
    return state[1:] + (w,)

def cumfreqs(chain, state):
    choices, weights = zip(*chain.model[state].items())
    sw = np.cumsum(np.array(weights, dtype=float))
    sw /= sw[-1]
    return (choices, np.concatenate(([0], sw)))


init_state = 2*(BEGIN,) #El numero depen de state_size
n=0.165489445 #Numero que surt de l'Arithmetic coding. 9 decimals funciona guai
word='Hola'
while word != END:
    chs, fq = cumfreqs(chain, init_state)
    for i in range(len(fq)-1):
        if fq[i] <= n < fq[i+1]: break
    #fq[i], fq[i+1], chs[i]
    #Actulaitzem pel següent pas
    init_state = move(init_state, chs[i])
    n = (n - fq[i])/float(fq[i+1]-fq[i])
    word = chs[i]
    print(word)
