#!python3

import ZipScraper

scrape = ZipScraper.ZipScraper()

while True:
    print("Make a selection to continue:")
    print("1. Scrape all zip codes")
    print("2. Scrape a state's zip code")
    print("3. Add zip code data to database")

    try:
        choice = int(input("Choice: "))

    except ValueError:
        print("Invalid selection. Please choose another.\n")

    except KeyboardInterrupt:
        print("Exiting...\n")
        break
