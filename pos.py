import nltk
from nltk import word_tokenize



text = word_tokenize("They refuse to permit us to obtain the refuse permit")
nltk.pos_tag(text)

