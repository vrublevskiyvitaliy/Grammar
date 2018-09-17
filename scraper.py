from selenium import webdriver
import time

MAIN_URL = "http://nlp.stanford.edu:8080/parser/index.jsp"


def get_driver():
    driver = webdriver.Chrome('/Users/vitaliyvrublevskiy/projects/Grammar/bin/chromedriver')
    return driver


def get_sentences():
    return [
        'My dog also likes eating sausage.',
        'Please enter a sentence to be parsed.'
    ]


def get_data(s, driver):
    queryField = driver.find_element_by_id('query')
    queryField.clear()
    queryField.send_keys(s)
    parseButton = driver.find_element_by_id('parseButton')
    parseButton.submit()
    time.sleep(5)
    parseTree = driver.find_element_by_id('parse')
    return parseTree.text
    y = 0


def scrap():
    driver = get_driver()
    for s in get_sentences():

        driver.get(MAIN_URL)
        time.sleep(5)
        data = get_data(s, driver)
        time.sleep(5)

if __name__ == "__main__":
    scrap()