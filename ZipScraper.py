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

        stateIdx = 0
        tmp = b.find_elements_by_class_name('stateLink')  # enumerate links for each state
        states = []

        # enumerate state names in text format for later display
        for state in tmp:
            states.append(state.text)

        trElem = 3  # for identifying tr xpath element. starts at 3 on each page

        f = open(self.outFileName, 'w', newline='')  # open csv file to write to it
        outWriter = csv.writer(f)  # create csv writer object to write to file

        outWriter.writerow(["zip code", "city", "county", "state"])

        for state in states:
            b.find_element_by_link_text(state).click()  # click current link for state

            try:
                while True:
                    # parse zip code, city, and county
                    zipCode = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']/td[1]')

                    city = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']/td[2]')

                    county = b.find_element_by_xpath('id("leftCol")/table[1]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr['+str(trElem)+']/td[3]')

                    outWriter.writerow([zipCode.text, city.text, county.text, state])  # write row of data

                    """# debug
                    print(zipCode.text)
                    print(city.text)
                    print(county.text)
                    print()"""

                    trElem += 1  # increment trElem to move to next row in the table

            except NoSuchElementException:
                print(states[stateIdx] + ' ' + '(' + " complete.")

                trElem = 3  # reset trElem for next table of zip codes

                stateIdx += 1

                sleep(1.5)  # short wait so as not to spam the server

                b.get(self.START)  # return to starting list of all state links

        self.completionMessage()
        f.close()  # close CSV file when done
        b.close()  # close browser when done

    def completionMessage(self):
        print("Scrape complete")
