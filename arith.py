import markovify

text = u"Example phrase. This is another example sentence. And another one"
text_model = markovify.Text(text)
chain = text_model.chain

# My initial state
from markovify.chain import BEGIN
ini_state = tuple(2* [BEGIN])


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
