from nltk.tokenize import sent_tokenize

# def get_sentances():
#     file = open('/Users/vitaliyvrublevskiy/projects/Grammar/data/moby.txt', 'r')
#     #print file.read()
#     text = file.read().decode('utf-8')
#     sent_tokenize_list = sent_tokenize(text)
#     return sent_tokenize_list[300:]

import nltk
nltk.download('punkt')

def get_sentances():
    file = open('/Users/vrublevskyi/Uni/Grammar/data/jfleg_part.txt', 'r')
    text = file.read().decode('utf-8')
    sent_tokenize_list = text.split("\n")
    return sent_tokenize_list