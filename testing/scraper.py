from selenium import webdriver
import data
import time
from nltk.corpus import brown


MAIN_URL = "http://nlp.stanford.edu:8080/parser/index.jsp"


def get_driver():
    driver = webdriver.Chrome('/Users/vitaliyvrublevskiy/projects/Grammar/bin/chromedriver')
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
    for sent in brown.sents(categories=['reviews'])[100:]:
        s = ' '.join(sent)
        print s
        try:
            driver.get(MAIN_URL)
            time.sleep(5)
            data = get_data(s, driver)
            with open("brown-tree.txt", "a") as myfile:
                myfile.write(data + '\n')
            time.sleep(5)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    scrap()