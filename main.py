import sys
import time
from io import open
from os import system
from bs4 import BeautifulSoup
from os import name as osName
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class LoggingPrinter:
    def __init__(self, filename):
        self.out_file = open(filename, "w", encoding='utf-8')
        self.old_stdout = sys.stdout
        sys.stdout = self
    def write(self, text):
        self.old_stdout.write(text)
        self.out_file.write(text)
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        sys.stdout = self.old_stdout

def clear():
    if osName == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def find(word, filename):
    with open(filename) as file:
        for line in file:
            if word in line:
                print(line, end='')

def main():
    while True:
        num = input("Enter the page or print exit:\n>>")
        if 0 < int(num) < 15:
            url = "https://coinmarketcap.com/?page=" + str(num)
        else:
            print("This page doesnt exist")
        if num == "exit":
            return 0


        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        driver.get(url)
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        percent = 0.1
        clear()
        print("Loading...")
        while percent <= 1:
            driver.execute_script("window.scrollTo(0, " + str(scroll_height * percent) + ");")
            time.sleep(0.1)
            percent += 0.1


        bsoup = BeautifulSoup(driver.page_source, 'html.parser')
        table = bsoup.find('table', class_='cmc-table')
        crypttable = table.find('tbody').find_all('tr', class_='')

        with LoggingPrinter("coin.txt"):
            print('{:<3}'.format("#"),
                  '{:>40}'.format("Name"),
                  '{:<20}'.format(" "),
                  '{:<15}'.format("Price"),
                  '{:<25}'.format("Market Cap"))

            for crypt in crypttable:
                properties = crypt.find_all('td')
                block = properties[2].find_all('p')
                numberPlate = properties[1].find('p')
                name = block[0]
                reduct = block[1]
                price = properties[3].find('a')
                marketCap = properties[6].find('p')

                print('{:<4}'.format(numberPlate.text), "|",
                      '{:45}'.format(name.text),
                      '{:>6}'.format(reduct.text), "|",
                      '{:>15}'.format(price.text), "|",
                      '{:>20}'.format(marketCap.text))
        while True:
            word = input("Enter cryptocoin name or 'exit'\n>>")
            find(word, "coin.txt")
            if word == "exit":
                return 0

if __name__ == '__main__':
    main()