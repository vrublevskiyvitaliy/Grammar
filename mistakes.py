import nltk
from nltk import word_tokenize




def main():

    sentances = [
        'I go home.',
        'I went home.',
        'I gone home.',
        'I has gone home.',
    ]

    for s in sentances:
        print build_sentence(s)

main()