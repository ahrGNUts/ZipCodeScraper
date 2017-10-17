from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv

class ZipScraper:

    def __init__(self):
        print("Initializing...")
        self.START = 'http://www.zipcodestogo.com/ZIP-Codes-by-State.htm'  # URL for main starting point
        self.outFileName = 'zipcodes.csv'  # output file name

        # test if file exists, create if it doesn't
        try:
            with open(self.outFileName, "r") as f:
                print("CSV file found!")
        except IOError:
            print("CSV file not found! Creating now...")
            with open(self.outFileName, "a") as f:
                print("File created successfully!")

        print("Scraper initialized.")

    def beginScraping(self):

        b = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        b.get(self.START)  # go to starting URL

        states = b.find_elements_by_class_name('stateLink')  # enumerate links for each state

        trElem = 3  # for identifying tr xpath element. starts at 3 on each page

        for state in states:
            state.click()  # click current link for states

            try:
                # parse
                while True:
                    # parse zip code, city, and county
                    zipCode = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[1]')

                    city = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[2]')

                    county = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']+td[3]')

                    with open(self.outFileName, 'w', newline='') as f:
                        outWriter = csv.writer(f)  # create writer object for writing to csv

                        outWriter.writerow([zipCode, city, county])  # write row of data

                    trElem += 1  # increment trElem to move to next row in the table

                    sleep(1.5)  # short wait so as not to spam the server

            except NoSuchElementException:
                print(state.text + " complete.")

                trElem = 3  # reset trElem for next table of zip codes

                sleep(1.5)  # short wait so as not to spam the server

                b.get(self.START)  # return to starting list of all state links

        b.close()  # close browser when done


