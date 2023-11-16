from selenium import webdriver
import data
import time
from pycorenlp import StanfordCoreNLP

MAIN_URL = "http://nlp.stanford.edu:8080/parser/index.jsp"


def get_driver():
    driver = webdriver.Chrome('/Users/vrublevskyi/Uni/Grammar/bin/chromedriver')
    return driver


def get_sentences():
    return data.get_sentances()


def get_data(s, driver):
    queryField = driver.find_element_by_id('query')
    queryField.clear()
    queryField.send_keys(s)
    parseButton = driver.find_element_by_id('parseButton')
    parseButton.submit()
    time.sleep(5)
    parseTree = driver.find_element_by_id('parse')
    text = parseTree.text
    text = text.replace('\n','')
    text = text.replace('\t','')
    return text

def scrap():
    driver = get_driver()
    for s in get_sentences():
        try:
            driver.get(MAIN_URL)
            time.sleep(5)
            data = get_data(s, driver)
            with open("tree_jfleg_part.txt", "a") as myfile:
                myfile.write(data + '\n')
            time.sleep(5)
        except:
            pass

def scrap_locally():
    nlp = StanfordCoreNLP('http://localhost:9000')

    for s in get_sentences():
            s = s.encode('ascii', 'ignore')
            output = nlp.annotate(s, properties={
                'annotators': 'parse',
                'outputFormat': 'json'
            })
            data = output['sentences'][0]['parse']
            data = data.replace("\n", '')

            print data
            with open("tree_jfleg_part.txt", "a") as myfile:
                myfile.write(data + '\n')
            myfile.close()



    # text = "The old oak tree from India fell down."
    #
    # output = nlp.annotate(text, properties={
    #     'annotators': 'parse',
    #     'outputFormat': 'json'
    # })
    #
    # print(output['sentences'][0]['parse'])

if __name__ == "__main__":
    # scrap()
    scrap_locally()