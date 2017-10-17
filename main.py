#!python3

import ZipScraper
from sys import exit

scraper = ZipScraper.ZipScraper()


# where the magick happens
# print
def main():
    while True:
        printMainMenu()

        try:
            choice = int(input("Choice: "))

            if choice == 1:
                scraper.beginScraping()
            elif choice == 2 or 3:
                print("Under construction. Make another selection.")
            elif choice == 4:
                exitAndClose()
            else:
                invalidSelectionMessage()

        except ValueError:
            invalidSelectionMessage()

        except KeyboardInterrupt:
            exitAndClose()


# print exit message an close the script
def exitAndClose():
    print("Exiting...\n")
    exit(0)


# for when silly fingers/intentional malice/bots getting smarter/etc.
def invalidSelectionMessage():
    print("Invalid selection. Please choose another.\n")


def printMainMenu():
    print("\nMake a selection to continue:")
    print("1. Scrape all zip codes")
    print("2. Scrape a state's zip code")
    print("3. Add zip code data to database")
