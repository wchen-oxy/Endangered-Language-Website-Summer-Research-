import os
import sys
from nltk.tokenize import word_tokenize
import nltk

file = '/Users/Work/Documents/Coding/Ongoing/Final Bhutia/venv/lib/python3.6/site-packages'
sys.path.append(file)

text1 = "It's true that the chicken was the best bamboozler in the known multiverse."
tokens = word_tokenize(text1)
print(tokens)