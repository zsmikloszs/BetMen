from magicScraper import *

if __name__ == '__main__':
    #
    print('Starting to Scrape admiral')

    ### ADMIRAL
    LINK = 'https://www.admiral.ro/ro/sporturi#sports-hub/football/romania/liga_i'
    rows = "//li[@class='KambiBC-sandwich-filter__event-list-item']"
    Scrape(LINK, rows)

    print('Finished Scraping admiral')
