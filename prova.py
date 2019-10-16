

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import textacy
from textacy.datasets import Wikipedia
from collections import Counter, defaultdict
import warnings; warnings.simplefilter('ignore')
import markovify

# # graficos incrustados
# %matplotlib inline


# def leer_texto(texto):
    # """Funcion auxiliar para leer un archivo de texto"""
    # with open(texto, 'r') as text:
        # return text.read()

# wp = Wikipedia(lang='es', version='latest')
# wp.download()
# wp.info
# for text in wp.texts(min_len=1000, limit=2):
    # print(text[:375], "\n")
        
"""
Creates a corpus from Wikipedia dump file.
Inspired by:
https://github.com/panyang/Wikipedia_Word2vec/blob/master/v1/process_wiki.py
"""
# pip install gensim
import sys
from gensim.corpora import WikiCorpus

def make_corpus(in_f, out_f):

	"""Convert Wikipedia xml dump file to text corpus"""

	output = open(out_f, 'w')
	wiki = WikiCorpus(in_f)

	i = 0
	for text in wiki.get_texts():
		output.write(bytes(' '.join(text), 'utf-8').decode('utf-8') + '\n')
		i = i + 1
		if (i % 10000 == 0):
			print('Processed ' + str(i) + ' articles')
	output.close()
	print('Processing complete!')


if __name__ == '__main__':

	if len(sys.argv) != 3:
		print('Usage: python make_wiki_corpus.py <wikipedia_dump_file> <processed_text_file>')
		sys.exit(1)
	in_f = sys.argv[1]
	out_f = sys.argv[2]
	make_corpus(in_f, out_f)  
        











# # Get raw text as string.
# with open("/home/USERS/roger.casals.valldeoriola/KOLMOGOROV/MMT/Text.txt") as f:
    # text = f.read()

# # Build the model.

# text_model = markovify.Text(text, state_size=2)
# # Print five randomly-generated sentences
# for i in range(10):
    # print(text_model.make_sentence())

# # Print three randomly-generated sentences of no more than 280 characters
# for i in range(5):
    # print(text_model.make_short_sentence(280))
