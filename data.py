from nltk.tokenize import sent_tokenize

def get_sentances():
    file = open('/Users/vitaliyvrublevskiy/projects/Grammar/data/moby.txt', 'r')
    #print file.read()
    text = file.read().decode('utf-8')
    sent_tokenize_list = sent_tokenize(text)
    return sent_tokenize_list[300:]

