from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv

class ZipScraper:

    def __init__(self):
        self.b = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.START = 'http://www.zipcodestogo.com/ZIP-Codes-by-State.htm'
        self.stateIdx = 0
        self.states = []
        self.outFileName = 'zipcodes.csv'

    def beginScraping(self):
        self.b.get(self.START)  # go to starting URL

        self.states = self.b.find_elements_by_class_name('stateLink')  # enumerate links for each state

        trElem = 3  # for identifying tr xpath element. starts at 3 on each page

        for state in self.states:
            state.click()  # click current link for states

            try:
                # parse
                while True:
                    # parse zip code, city, and county
                    zipCode = self.b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[1]')

                    city = self.b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[2]')

                    county = self.b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[3]')

                    with open(self.outFileName, 'w', newline='') as f:
                        outWriter = csv.writer(f)  # create writer object for writing to csv

                        outWriter.writerow([zipCode, city, county])  # write row of data

                    trElem += 1  # increment trElem to move to next row in the table

            except NoSuchElementException:
                print(state.text + " complete.")

                trElem = 3  # reset trElem for next table of zip codes

                self.b.get(self.START)  # return to starting list of all state links


